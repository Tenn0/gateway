
import asyncio
import json
import struct
import sys
import logging
from .ble_gateway import gateway
from TheengsDecoder import getProperties, getAttribute

class discovery(gateway):
    def __init__(self, broker, port, username, password, discovery, discovery_topic):
      super().__init__(broker, port, username, password)
      self.discovery = discovery
      self.discovery_topic = discovery_topic

    def connect_mqtt(self):
        super().connect_mqtt()
    
    def publish(self, msg, pub_topic):
        return super().publish(msg, pub_topic)
    
    def publish_device_info(self, pub_device):  ##publish sensor directly to home assistant via mqtt discovery
        print(f"publishing device `{pub_device}`")
        pub_device = pub_device
        print(type(pub_device))
        print(pub_device.keys())

        hadevice = {}
        hadevice['name'] = pub_device['name']
        hadevice['manufacturer'] = pub_device['brand']
        ha = hadevice
        device = {}
        ##setup HA device
        
        pub_device_uuid = pub_device['id']
        pub_device_uuid = pub_device_uuid.replace(':', '')
        device['unique_id'] = pub_device['id']
        topic = "lol" + "/" + pub_device_uuid
        state_topic = topic + "/state"
        config_topic = topic + "/config"
        attr_topic = topic + "/attributes"
        if 'name' in pub_device:
          device['name'] = pub_device['name']
        else: 
            device['name'] = pub_device_uuid
        device['state_topic'] = state_topic
        device['device'] = ha
        device['schema'] = "json"
        device['state_topic'] = state_topic
        data = getProperties(pub_device['model_id'])
        data = json.loads(data)
        data = data['properties']
        print(data.keys())
        for k in data.keys():
                  print(data)
                  print(k)

                  if data['name']:
                    print(f"property: {k['name']}: {pub_device[k]} {k}")
        msg = pub_device['properties']
        self.publish(msg, state_topic) 
        
        ##attributes
        attributes = {}      
        attributes['rssi'] = pub_device['rssi']
        attributes['brand'] = pub_device['brand']
        attributes['id'] = pub_device['id']
        attributes['model'] = pub_device['model']
        attributes['model_id'] = pub_device['model_id']
        attributes['unit_of_meas'] = pub_device['attributes']
        attributes = json.dumps(attributes)
        device['json_attr_t'] = attr_topic
        self.publish(attributes, attr_topic) ##attributes
        
        
        payload = json.dumps(device)
        msg = payload
        self.publish(msg, config_topic) ##overall device

    def returnValues(self, device):
      properties = {}
      device = json.loads(device)
      device = device['model_id']
      properties = getProperties(device)
      print(properties)
