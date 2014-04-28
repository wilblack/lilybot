
class JJBot(object):
    pass

    def __init__(self):
        self.commands = []
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




    # if message == 'u' :
    #             self.log("Running Forward")
    #             BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
            
    #         elif message == 'd' :
    #             self.log("Running Reverse")
    #             BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
            
    #         elif message == 'r' :
    #             self.log("Turning Right")
    #             BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
            
    #         elif message == 'l' :
    #             self.log("Turning Left")
    #             BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
            
    #         elif message == 'b' :
    #             self.log("New Stopped")
    #             BrickPi.MotorSpeed[PORT_A] = 0
    #             BrickPi.MotorSpeed[PORT_D] = 0

    #         # Wil's added capabilites
    #         elif message == "nl":
    #             self.log("Nudge Left")
    #             BrickPi.MotorSpeed[PORT_A] = 0  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
    #             time.sleep(.5)
    #             BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
              
    #         elif message == "nr":
    #             self.log("Nudge Right")
    #             BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = 0  #Set the speed of MotorA (-255 to 255)
    #             time.sleep(.5)
    #             BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
    #             BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)


    #         elif message == "ll":
    #             self.log("Look Left")
    #             BrickPi.MotorSpeed[PORT_C] = -1*self.LOOK_SPEED
    #             time.sleep(self.LOOK_DT)
    #             # BrickPi.MotorSpeed[PORT_C] = -1*self.LOOK_SPEED
    #             # time.sleep(self.LOOK_DT)
    #             BrickPi.MotorSpeed[PORT_C] = 0

    #         elif message == "lr":
    #             self.log("Look Right")
    #             BrickPi.MotorSpeed[PORT_C] = self.LOOK_SPEED
    #             time.sleep(self.LOOK_DT)
    #             # BrickPi.MotorSpeed[PORT_C] = self.LOOK_SPEED
    #             # time.sleep(self.LOOK_DT)
    #             BrickPi.MotorSpeed[PORT_C] = 0

    #         elif message == "start-camera-1":  # Shutdown
    #             self.log("Starting camera")
    #             try:
    #                 self.bot.startCamera()
    #             except Exception, e: 
    #                 print e

    #         elif message == "stop-camera-1":  # Stop camera
    #             self.log("Stopping Camera")
    #             self.bot.stopCamera()


    #         elif message == "x":  # Shutdown
    #             self.log("Shutting down")
    #             shutdown()
    #         elif message == "y":  # Shutdown
    #             restart()
            
    #         BrickPiUpdateValues()                # BrickPi updates the values for the motors