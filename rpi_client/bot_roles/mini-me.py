import time
import subprocess

from bot_roles.core import Core

try:
    from BrickPi import *   #import BrickPi.py file to use BrickPi operations
except:
    pass


class MiniMe(Core):


    def __init__(self, socket):
        super(MiniMe, self).__init__(socket)

        self.commands = ['stop',
                         'left',  # Port A
                         'right',
                         'up',    # Port B
                         'down']

        self.LOOK_SPEED = 255
        self.LOOK_DT = 0.6
        self.NUDGE_DT = 0.3


    def stop():
        BrickPi.MotorSpeed[PORT_A] = 0  # Pan
        BrickPi.MotorSpeed[PORT_B] = 0  # Tilt

    def left(self, kwargs):
        print "!!!!! FORWARD !!!!!"
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        time.sleep(2)
        self.stop()

    def right(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = -255  #Set the speed of MotorA (-255 to 255)

    def left(self, kwargs):
        print "!!!!! FORWARD !!!!!"
        BrickPi.MotorSpeed[PORT_B] = 255  #Set the speed of MotorA (-255 to 255)

    def right(self, kwargs):
        BrickPi.MotorSpeed[PORT_B] = -255  #Set the speed of MotorA (-255 to 255)


