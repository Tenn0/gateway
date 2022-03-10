
import asyncio
import json
import struct
import sys
import logging

from bleak import BleakScanner
from threading import Thread
from decoder import decodeBLE, getProperties, getAttribute

class test:

  
  async def ble_scan_loop(self):
          scanner = BleakScanner()
          scanner.register_detection_callback(detection_callback)
 #         logger.info('Starting BLE scan')
          running = True
          while not self.stopped:
              try:
                  if self.client.is_connected():
                      await scanner.start()
                      await asyncio.sleep(self.scan_time)
                      await scanner.stop()
                      await asyncio.sleep(self.time_between_scans)
                  else:
                      await asyncio.sleep(5.0)
              except Exception as e:
                raise e
    
#        logger.error('BLE scan loop stopped')
          running = False

def detection_callback(device, advertisement_data):
  #    logger.debug("%s RSSI:%d %s" % (device.address, device.rssi, advertisement_data))
       data_json = {}

       if advertisement_data.service_data:
          dstr = list(advertisement_data.service_data.keys())[0]
          data_json['servicedatauuid'] = dstr[4:8]
          dstr = str(list(advertisement_data.service_data.values())[0].hex())
          data_json['servicedata'] = dstr

       if advertisement_data.manufacturer_data:
          dstr = str(struct.pack('<H', list(advertisement_data.manufacturer_data.keys())[0]).hex())
          dstr += str(list(advertisement_data.manufacturer_data.values())[0].hex())
          data_json['manufacturerdata'] = dstr

       if advertisement_data.local_name:
          data_json['name'] = advertisement_data.local_name

       if data_json:
          data_json['id'] = device.address
          data_json['rssi'] = device.rssi
          data_json = decodeBLE(json.dumps(data_json))

       if data_json:
          print(data_json)
          dev = json.loads(data_json)
          data = getProperties(dev['model_id'])
          print(data.keys)
          print(device.keys())

def run(arg):
    global gw
    
    gw = test()
    

    gw.scan_time = 5
    gw.time_between_scans = 5
 
    loop = asyncio.get_event_loop()
    t = Thread(target=loop.run_forever, daemon=True)
    t.start()
    asyncio.run_coroutine_threadsafe(gw.ble_scan_loop(), loop)

    gw.connect_mqtt()

    try:
        gw.client.loop_forever()
    except(KeyboardInterrupt, SystemExit):
        gw.client.disconnect()
        gw.stopped = True
        while gw.running:
            pass
        loop.call_soon_threadsafe(loop.stop)
        t.join()
    
if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} /path/to/config_file")
    run(arg)