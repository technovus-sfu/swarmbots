from xinput import *
import time
import serial
import string
import math

robo1 = serial.Serial('COM6',9600)
robo1.flushInput()

# return a bytes
# maintains same ratio of value to max, with different max. 
def ratio_to_new_size(value, sourceLength, newLength):

    value = abs(value)

    if sourceLength >= newLength:
        value = int(value / pow(2, sourceLength - newLength))
    else:
        value = int(value * pow(2, newLength - sourceLength))

    return value 

def transmit_axis(type, value):
    indicator = 0
    if type == 'l_thumb_y':
        if value > 0:
            indicator = 1
        else:
            indicator = 4
    if type == 'r_thumb_y':
        if value > 0:
            indicator = 2
        else:
            indicator = 3

    #if thumb axis
    if type != 'left_trigger' and type != 'right_trigger':
        value = ratio_to_new_size(value, 15, 8)

    robo1.write(indicator.to_bytes(1,byteorder='big'))
    #print(indicator.to_bytes(1,byteorder='big'))
    robo1.write(value.to_bytes(1,byteorder='big'))
    #print(value.to_bytes(1,byteorder='big'))

    # print(bytearray(indicator.to_bytes(1,byteorder='big')).append(value))
    
def joystick_readout():
    joysticks = XInputJoystick.enumerate_devices()
    
    for stick in joysticks:
        
        @stick.event
        def on_button(button, pressed):
            print('Joystick',stick.device_number,'button',button,' state:', pressed)



        @stick.event
        def on_axis(axis, value):
            print('Joystick',stick.device_number,'axis',axis ,value)
            transmit_axis(axis, value)

    while True:
        for stick in joysticks:
            stick.dispatch_events()


# transmit_axis('r_thumb_y',32767)
# # time.sleep(1)
# transmit_axis('l_thumb_y',32767)
# time.sleep(1)
# transmit_axis('r_thumb_y',-6160)
# # time.sleep(1)
# transmit_axis('l_thumb_y',-6160)
joystick_readout()