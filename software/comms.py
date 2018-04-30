import serial
import string

address1 = 'COM6'

robo1 = serial.Serial(address1,9600)

robo1.flushInput()

while 1:
	key = input()
	robo1.write(key.encode('utf-8'))
	if key == 'q':
		exit