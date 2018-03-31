from xinput import *

def joystick_readout():
    joysticks = XInputJoystick.enumerate_devices()

    for stick in joysticks:
        @stick.event
        def on_button(button, pressed):
            print('Joystick',stick.device_number,'button',button,' state:', pressed)

        @stick.event
        def on_axis(axis, value):
            print('Joystick',stick.device_number,'axis',axis,"{:1.4f}".format(value))

    while True:
        for stick in joysticks:
            stick.dispatch_events()

joystick_readout()