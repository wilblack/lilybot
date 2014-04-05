"""
This module starts the ardyh client on a Raspberry Pi.

Written by Wil Black wilblack21@gmail.com Apr, 5 2014
"""

from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop


class Ardyh(TornadoWebSocketClient):
    """
    Web Socket client to connect to ardyh on start up.
    """

    def __init__(self, uri, protocols):
        rs = super(Ardyh, self).__init__(uri, protocols)
        
        self.ARDYH_URI = 'ws://173.255.213.55:9093/ws'
        self.LOG_DTFORMAT = "%H:%M:%S"

        try:
            self.bot = JJBot()
            self.LOOK_SPEED = 80
            self.LOOK_DT = 0.5
        except:
            "JJBot module not found not."

        return rs


    def opened(self):
        mac = self.get_mac_address()

        # Tells ardyh that is a new connection
        out = {"new":"", "camera_port":8080}
        self.send(json.dumps(out))

        msg = "%s: Hello. I 'm a lilybot" %(mac)

        sensors = tornado.ioloop.PeriodicCallback(self.loopCallback, 500)
        sensors.start()

        self.send(msg)


    def received_message(self, message):
        
        message = unicode(message)
        
        import pdb; pdb.set_trace()

        if message == 'u' :
            self.log("Running Forward")
            BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
        
        elif message == 'd' :
            self.log("Running Reverse")
            BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
        
        elif message == 'r' :
            self.log("Turning Right")
            BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
        
        elif message == 'l' :
            self.log("Turning Left")
            BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
        
        elif message == 'b' :
            self.log("New Stopped")
            BrickPi.MotorSpeed[PORT_A] = 0
            BrickPi.MotorSpeed[PORT_D] = 0

        # Wil's added capabilites
        elif message == "nl":
            self.log("Nudge Left")
            BrickPi.MotorSpeed[PORT_A] = 0  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
            time.sleep(.5)
            BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
          
        elif message == "nr":
            self.log("Nudge Right")
            BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = 0  #Set the speed of MotorA (-255 to 255)
            time.sleep(.5)
            BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
            BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)


        elif message == "ll":
            self.log("Look Left")
            BrickPi.MotorSpeed[PORT_C] = -1*self.LOOK_SPEED
            time.sleep(self.LOOK_DT)
            # BrickPi.MotorSpeed[PORT_C] = -1*self.LOOK_SPEED
            # time.sleep(self.LOOK_DT)
            BrickPi.MotorSpeed[PORT_C] = 0

        elif message == "lr":
            self.log("Look Right")
            BrickPi.MotorSpeed[PORT_C] = self.LOOK_SPEED
            time.sleep(self.LOOK_DT)
            # BrickPi.MotorSpeed[PORT_C] = self.LOOK_SPEED
            # time.sleep(self.LOOK_DT)
            BrickPi.MotorSpeed[PORT_C] = 0

        elif message == "start-camera-1":  # Shutdown
            self.log("Starting camera")
            try:
                self.bot.startCamera()
            except Exception, e: 
                print e

        elif message == "stop-camera-1":  # Stop camera
            self.log("Stopping Camera")
            self.bot.stopCamera()


        elif message == "x":  # Shutdown
            self.log("Shutting down")
            shutdown()
        elif message == "y":  # Shutdown
            restart()
        
        BrickPiUpdateValues()                # BrickPi updates the values for the motors



    def closed(self, code, reason=None):
        ioloop.IOLoop.instance().stop()


    def log(self, message):
        now = dt.now().strftime(LOG_DTFORMAT)
        message = "[%s] %s" %(now, message)
        print message
        self.send(message)


    def loopCallback(self):
        sensor_values = self.bot.get_sensors_values()
        out = {"sensor_values":sensor_values}

        self.send(json.dumps(out))


    def get_mac_address(self):
        mac = get_mac()
        return "%012X"%mac


if __name___ == "":

    # Start streaming data to ardyh.
    ardyh = Ardyh(ARDYH_URI, protocols=['http-only', 'chat'])
    ardyh.connect()