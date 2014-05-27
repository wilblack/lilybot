import time
from BrickPi import *   #import BrickPi.py file to use BrickPi operations

class JJBot(object):
    pass

    def __init__(self):
        self.commands = ['forward', 
                         'stop', 
                         'reverse', 
                         'nudge_left', 
                         'nudge_right', 
                         'steer_left',
                         'steer_right',
                         'look_up',
                         'look_down']


        self.LOOK_SPEED = 80
        self.LOOK_DT = 0.5
        
        # try:
        #         print "Trying to load JJBot"
        #         self.bot = JJBot()
        #         self.LOOK_SPEED = 80
        #         self.LOOK_DT = 0.5
        #         self.JJBOT = True
        #     except:
        #         print "[WARNING] JJBot module not found not."
        #         self.JJBOT = False
        #     return rs



        
        # try:
        #     "Trying to start sensors"
        #     sensors = tornado.ioloop.PeriodicCallback(self.loopCallback, 500)
        #     sensors.start()
        # except:
        #     "[WARNING] Sensors not started"

        # # Tells ardyh that is a new connection
        # out = {"new":"", "camera_port":8080}
        # self.send(out)




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
        BrickPi.MotorSpeed[PORT_A] = -255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()

    def steer_right(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = -255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()


    def nudge_left(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 0  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()
        time.sleep(.5)
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()

    def nudge_right(self, kwargs):
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 0  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()
        time.sleep(.5)
        BrickPi.MotorSpeed[PORT_A] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPi.MotorSpeed[PORT_D] = 255  #Set the speed of MotorA (-255 to 255)
        BrickPiUpdateValues()

    def look_up(self, kwargs):
        BrickPi.MotorSpeed[PORT_B] = -1*self.LOOK_SPEED
        time.sleep(self.LOOK_DT)
        BrickPi.MotorSpeed[PORT_B] = 0
        BrickPiUpdateValues()

    def look_down(self, kwargs):
        BrickPi.MotorSpeed[PORT_B] = self.LOOK_SPEED
        time.sleep(self.LOOK_DT)
        BrickPi.MotorSpeed[PORT_B] = 0
        BrickPiUpdateValues()

    def start_camera_1(self, kwargs):
        try:
            self.bot.startCamera()
        except Exception, e: 
            print e

    def stop_camera_1(self, kwargs):
        try:
            self.bot.stopCamera()
        except Exception, e:
            print e
            
    #                         # BrickPi updates the values for the motors