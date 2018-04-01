from xinput import *
import serial
import string

robo1 = serial.Serial('COM5',9600,write_timeout=1.0)
robo1.flushInput()
robo1.write(ord('w'))

def joystick_readout():
    
    #robo2 = serial.Serial(address2,9600)
    joysticks = XInputJoystick.enumerate_devices()
    
    for stick in joysticks:
        
        @stick.event
        def on_button(button, pressed):
            print('Joystick',stick.device_number,'button',button,' state:', pressed)

        @stick.event
        def on_axis(axis, value):
            print('Joystick',stick.device_number,'axis',axis,"{:1.4f}".format(value))
            if axis == 'l_thumb_y':
                if value > 0:
                    robo1.write('w')
                else:
                    robo1.write('s')
            if axis == 'l_thumb_x':
                if value > 0:
                    robo1.write('d')
                else:
                    robo1.write('a')
            robo1.flushInput()

    while True:
        for stick in joysticks:
            stick.dispatch_events()

#joystick_readout()