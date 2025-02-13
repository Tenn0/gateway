"""
  TheengsGateway - Decode things and devices and publish data to an MQTT broker

    Copyright: (c)Florian ROBERT

    This file is part of TheengsGateway.

    TheengsGateway is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TheengsGateway is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import json
import argparse
from .ble_gateway import run

default_config = {
    "host":"",
    "port":1883,
    "user":"",
    "pass":"",
    "ble_scan_time":5,
    "ble_time_between_scans":5,
    "publish_topic": "home/TheengsGateway/BTtoMQTT",
    "subscribe_topic": "home/TheengsGateway/+",
    "log_level": "WARNING",
    "discovery": False,
    "discovery_topic": "homeassistant/sensor",
    "discovery_device_name": "TheengsGateway"
}

conf_path = os.path.expanduser('~') + '/theengsgw.conf'

parser =  argparse.ArgumentParser()
parser.add_argument('-H', '--host', dest='host', type=str, help="MQTT host address")
parser.add_argument('-P', '--port', dest='port', type=int, help="MQTT host port")
parser.add_argument('-u', '--user', dest='user', type=str, help="MQTT username")
parser.add_argument('-p', '--pass', dest='pwd', type=str, help="MQTT password")
parser.add_argument('-pt', '--pub_topic', dest='pub_topic', type=str, help="MQTT publish topic")
parser.add_argument('-st', '--sub_topic', dest='sub_topic', type=str, help="MQTT subscribe topic")
parser.add_argument('-pa', '--publish_all', dest='publish_all', type=bool, help="Publish all beacons if true")
parser.add_argument('-sd', '--scan_duration', dest='scan_dur', type=int, help="BLE scan duration (seconds)")
parser.add_argument('-tb', '--time_between', dest='time_between', type=int, help="Seconds to wait between scans")
parser.add_argument('-ll', '--log_level', dest='log_level', type=str, help="TheengsGateway log level",
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
parser.add_argument('-Dt', '--discovery-topic', dest='discovery_topic', type=bool, help="MQTT Discovery for Home Assistant")
parser.add_argument('-D', '--discovery', dest='discovery', type=str, help="Home Assistant discovery Topic")
parser.add_argument('-Dn', '--discovery_name', dest='discovery_device_name', type=str, help="Device name for Home Assistant")
args = parser.parse_args()

try:
    with open(conf_path, 'r') as config_file:
        config = json.load(config_file)
except:
    config = default_config

if args.host:
    config['host'] = args.host
if args.port:
    config['port'] = args.port
if args.user:
    config['user'] = args.user
if args.pwd:
    config['pass'] = args.pwd
if args.pub_topic:
    config['publish_topic'] = args.pub_topic
if args.sub_topic:
    config['subscribe_topic'] = args.sub_topic
if args.publish_all:
    config['publish_all'] = args.publish_all
if args.scan_dur:
    config['ble_scan_time'] = args.scan_dur
if args.time_between:
    config['ble_time_between_scans'] = args.time_between
if args.log_level:
    config['log_level'] = args.log_level
if args.discovery:
    print("discovery arg given")
    print(args.discovery)
    if args.discovery == "false":
        print("Discovery disabled")
        config['discovery'] = "false"
    else:
        if args.discovery == "true":
          config['discovery'] = "true"
          if not args.discovery_topic:
             config['discovery_topic'] = default_config['discovery_topic']
          else:
            config['discovery_topic'] = args.discovery_topic
            config['discovery'] = "true"
            print("Discovery activated")
          if not args.discovery_device_name:
            if not 'discovery_device_name' in config.keys():
             config['discovery_device_name'] = default_config['discovery_device_name']

          if 'discovery_device_name' in config.keys():
             config['discovery_device_name'] = config['discovery_device_name']

else:
    print("discovery arg not given")
    if not 'discovery' in config.keys():
        config['discovery'] = "true"
        config['discovery_topic'] = default_config['discovery_topic']
        config['discovery_device_name'] = default_config['discovery_device_name']
    else:
        if config['discovery'] == "true":
           config['discovery'] = "true"
           print("Discovery enabled")
        else:
            if config['discovery'] == "false":
                config['discovery'] = "false"
                print("Discovery disabled")
            else:
                config['discovery'] = default_config['discovery']

if not config['host']:
    sys.exit('Invalid MQTT host')

try:
    with open(conf_path, 'w') as config_file:
        config_file.write(json.dumps(config, sort_keys=True, indent=4))
except:
    raise SystemExit('Unable to open config file')

run(conf_path)
