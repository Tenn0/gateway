
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
        pub_device['properties'] = json.loads(getProperties(pub_device['model_id']))
        pub_device['properties'] = pub_device['properties']['properties']
        print(type(pub_device))
        print(pub_device['properties'].keys())

        hadevice = {}
        hadevice['name'] = pub_device['name']
        hadevice['ids'] = pub_device['id'].replace(':', '')
        hadevice['manufacturer'] = pub_device['brand']
        ha = hadevice
        device = {}
        ##setup HA device
        
        pub_device_uuid = pub_device['id']
        pub_device_uuid = pub_device_uuid.replace(':', '')
        device['unique_id'] = pub_device['id']
        topic = self.discovery_topic + "/" + pub_device_uuid + "/"

        #setup entities:
        for p in pub_device['properties']:
          
          print(f"p: {p}")
          print(pub_device['properties'])
          state_topic = topic + p +"/state"
          config_topic = topic + p + "/config"
          attr_topic = topic + p + "/attributes"
          device['name'] = pub_device['name'] + "_" + device['unique_id'] + "_" + p
          device['state_topic'] = state_topic
          device['device'] = ha
          device['schema'] = "json"
          device['state_topic'] = state_topic
          data = getProperties(pub_device['model_id'])
          data = json.loads(data)
          data = data['properties']  ##attributes
          attributes = {}      
          attributes['rssi'] = pub_device['rssi']
          attributes['brand'] = pub_device['brand']
          attributes['id'] = pub_device['id']
          attributes['model'] = pub_device['model']
          attributes['model_id'] = pub_device['model_id']
        
          attributes = json.dumps(attributes)
          device['json_attr_t'] = attr_topic
          self.publish(attributes, attr_topic) ##attributes
          print(data.keys())
          for k in data.keys():
                  print(data)
                  print(f"k: {k}, type: {type(k)}")
                  #k = json.loads(k)

                  #if k['name']:
                  print(f"property: {k}: {pub_device[k]} {k}")
                  #attributes['unit_of_meas'] = pub_device['attributes']
                  msg = pub_device[k]
                  self.publish(msg, state_topic) 
        
      
        
        
          payload = json.dumps(device)
          msg = payload
          self.publish(msg, config_topic) ##overall device
