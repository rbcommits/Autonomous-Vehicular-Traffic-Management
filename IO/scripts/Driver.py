#!/usr/bin/python
import smbus
import time

i2c = smbus.SMBus(1)
DEVICE_ADDRESS = 0x0a
global turn_offset


def sendData(num):
	global turn_offset
	turn_offset = num

while True:
	# Register write control commands
	# Initializing byte 99
	i2c.write_byte(DEVICE_ADDRESS, 99)
	# vCom setting forward drive (0-255)
	i2c.write_byte(DEVICE_ADDRESS, 0)
	# sCom setting steering (127 (standby), 126-0(max) left, 128-255(max) right)
	i2c.write_byte(DEVICE_ADDRESS, 127 + turn_offset)
	time.sleep(0.1)
	pass
