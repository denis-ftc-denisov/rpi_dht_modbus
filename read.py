#!/usr/bin/env python3

import Adafruit_DHT
import json
import time
from collections import defaultdict
from threading import Thread
from pymodbus.constants import Endian
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
from pymodbus.payload import BinaryPayloadBuilder
import logging
import logging.handlers as Handlers

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


file = open('config.json', mode='r')
config = json.loads(file.read())
file.close()

def data_update(config, a):
	context = a[0]
	while True:
		for sensor in config['sensors']:
			# Sensor should be set to Adafruit_DHT.DHT11,
			# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
	
			if sensor['type'] == 'DHT22':
				sensor_type = Adafruit_DHT.DHT22
			elif sensor['type'] == 'DHT11':
				sensor_type = Adafruit_DHT.DHT11
			elif sensor['type'] == 'AM2302':
				sensor_type = Adafruit_DHT.AM2302
			else:
				raise Exception("Unknown sensor type: " + sensor['type'])

			pin = int(sensor['pin'])
			humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin)
			
			if humidity is not None and temperature is not None:
				builder_t = BinaryPayloadBuilder(byteorder=Endian.Big,
                                   wordorder=Endian.Big)
				builder_h = BinaryPayloadBuilder(byteorder=Endian.Big,
                                   wordorder=Endian.Big)
				builder_t.add_32bit_float(temperature)
				builder_h.add_32bit_float(humidity)
				context.setValues(4, int(sensor['address_t']), builder_t.to_registers())
				context.setValues(4, int(sensor['address_h']), builder_h.to_registers())
				log.info('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
			else:
				log.warn('Failed to get reading. Try again!')

store = ModbusSlaveContext(
        ir=ModbusSequentialDataBlock(0, [17]*100))
                                
context = ModbusServerContext(slaves=store, single=True)

thread = Thread(target=data_update, args=(config, context,))
thread.start()
    
StartTcpServer(context, identity=ModbusDeviceIdentification(), address=("0.0.0.0", config['port']))
    