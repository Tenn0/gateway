
import asyncio
import json
import struct
import sys
import logging
from .ble_gateway import gateway


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
        print("publishing device {pub_device}")
        device = {}
        device['name'] = "BLEGateway"
        device['identifiers'] = "BLEGateway"
        device['manufacturer'] = "theengs"
        ha = device
        device = {}
        ##setup HA device
        pub_device = json.loads(pub_device)
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
        device['device'] = ha.device
        device['schema'] = "json"
        device['state_topic'] = state_topic
        if 'steps' in pub_device:  ## sensor states for Xaomi Mi Band
          msg = pub_device['steps']
          self.publish(msg, state_topic) 
        
        ##attributes
        attributes = {}      
        attributes['rssi'] = pub_device['rssi']
        attributes['brand'] = pub_device['brand']
        attributes['id'] = pub_device['id']
        attributes['model'] = pub_device['model']
        attributes['model_id'] = pub_device['model_id']
        attributes = json.dumps(attributes)
        device['json_attr_t'] = attr_topic
        self.publish(attributes, attr_topic) ##attributes
        
        
        payload = json.dumps(device)
        msg = payload
        self.publish(msg, config_topic) ##overall device
