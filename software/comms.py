from xinput import *
import serial
import string

address1 = 'COM6'
robo1 = serial.Serial(address1,9600)
robo1.flushInput()

while 1:
	byte1 = 3
	byte2 = 255
	robo1.write(byte1.to_bytes(1, byteorder='big'))
	print(byte1.to_bytes(1, byteorder='big'))
	robo1.write(byte2.to_bytes(1, byteorder='big'))
	print(byte2.to_bytes(1, byteorder='big'))
	byte1 = 1
	byte2 = 255
	robo1.write(byte1.to_bytes(1, byteorder='big'))
	robo1.write(byte2.to_bytes(1, byteorder='big'))
