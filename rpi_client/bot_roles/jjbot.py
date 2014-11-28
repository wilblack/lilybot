import time
import subprocess

from bot_roles.core import Core

try:
    from BrickPi import *   #import BrickPi.py file to use BrickPi operations
except:
    pass


class JJBot(Core):


    def __init__(self, socket):
        super(JJBot, self).__init__(socket)

        self.commands = ['forward', 
                         'stop', 
                         'reverse', 
                         'nudge_left', 
                         'nudge_right', 
                         'steer_left',
                         'steer_right',
                         'look_up',
                         'look_down']

        self.LOOK_SPEED = 255
        self.LOOK_DT = 0.6
        self.NUDGE_DT = 0.3

    def forward(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()
            
    def reverse(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = -255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = -255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()

    def stop(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 0
        BrickPi.MotorSpeed[PORT_D] = 0
        BrickPiUpdateValues()

    def steer_left(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = -128  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 128  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()

    def steer_right(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 128  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = -128  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()


    def nudge_left(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 0  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()
        time.sleep(self.NUDGE_DT)
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()

    def nudge_right(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 0  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()
        time.sleep(self.NUDGE_DT)
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()

    def look_up(self, kwargs):
        BrickPi.MotorSpeed[PORT_B] = self.LOOK_SPEED
        time.sleep(self.LOOK_DT)
        BrickPi.MotorSpeed[PORT_B] = 0
        BrickPiUpdateValues()

    def look_down(self, kwargs):
        BrickPi.MotorSpeed[PORT_B] = -1*self.LOOK_SPEED
        time.sleep(self.LOOK_DT)
        BrickPi.MotorSpeed[PORT_B] = 0
        BrickPiUpdateValues()

    def start_camera_1(self, kwargs):
        """

        mkdir /tmp/stream
        raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0
        LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/jjbot/www"

        """
        print "In JJBot.startCamera()"
        if not os.path.exists(self.source_path):
            os.mkdir(self.source_path)

        print "Calling raspistill command"
        command = "raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0"
        process1 = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        print process1
        

        # print "Calling mjpg_streamer command"
        # command = 'LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/jjbot/www"'
        # process2 = subprocess.Popen(command.split(), stdout=subprocess.PIPE)



    def stop_camera_1(self, kwargs):
        try:
            self.bot.stopCamera()
        except Exception, e:
            print e
            
    #                         # BrickPi updates the values for the motors
