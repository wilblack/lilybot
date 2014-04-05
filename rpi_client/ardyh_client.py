"""
This module starts the ardyh client on a Raspberry Pi.

Written by Wil Black wilblack21@gmail.com Apr, 5 2014
"""

import json
from datetime import datetime as dt
from uuid import getnode as get_mac
from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop

import tornado.ioloop

VERBOSE = True

class ArdyhClient(TornadoWebSocketClient):
    """
    Web Socket client to connect to ardyh on start up.
    """

    def __init__(self, protocols, uri='ws://173.255.213.55:9093/ws'):
        rs = super(ArdyhClient, self).__init__(uri, protocols)
        
        self.ARDYH_URI = uri
        self.LOG_DTFORMAT = "%H:%M:%S"
        
        try:
            print "Loading RPi-LPD8806"
            from bootstrap import *
            self.CTENOPHORE = True
        except:
            print "[WARNING] RPi-LPD8806 bootstrap module not found"
        try:
            print "Trying to load JJBot"
            self.bot = JJBot()
            self.LOOK_SPEED = 80
            self.LOOK_DT = 0.5
            self.JJBOT = True
        except:
            print "[WARNING] JJBot module not found not."
            self.JJBOT = False
        return rs


    def opened(self):
        print "Connection to ardh is open"
        mac = self.get_mac_address()

        # Tells ardyh that is a new connection
        out = {"new":"", "camera_port":8080}
        self.send(json.dumps(out))

        msg = "%s: Hello. I 'm a lilybot" %(mac)
        self.send(msg)

        try:
            "Trying to start sensors"
            sensors = tornado.ioloop.PeriodicCallback(self.loopCallback, 500)
            sensors.start()
        except:
            "[WARNING] Sensors not started"

        

    def received_message(self, message):
        
        message = unicode(message)
        if VERBOSE: print "Received message: %s" %(message)

        if self.JJBOT:
            self.receive_message_jjbot(message)

        elif self.CTENOPHORE:
            self.receive_message_ctenophore(message)


    def closed(self, code, reason=None):
        print "Closed down", code, reason
        ioloop.IOLoop.instance().stop()


    def log(self, message):
        now = dt.now().strftime(self.LOG_DTFORMAT)
        message = "[%s] %s" %(now, message)
        print message
        self.send(message)


    def loopCallback(self):
        if self.JJBOT:
            sensor_values = self.bot.get_sensors_values()
            out = {"sensor_values":sensor_values}
            self.send(json.dumps(out))


    def get_mac_address(self):
        mac = get_mac()
        return "%012X"%mac

    def receive_message_ctenophore(self, message):
        if VERBOSE: print "this is a ctenophore message"
        
        if message == 'u' :
            anim = Wave(led, Color(255, 0, 0), 4)
            for i in range(led.lastIndex):
                anim.step()
                led.update()
            led.fillOff()

        elif message == 'd' :
            anim = Rainbow(led)
            for i in range(384):
                anim.step()
                led.update()
            led.fillOff()
            
        elif message == 'r' :
            pass

        elif message == "start-camera-1":  # Shutdown
            self.log("Starting lights")
            
        elif message == "stop-camera-1":  # Stop camera
            self.log("Stopping Lights")
            


    def receive_message_jjbot(self, message):
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

if __name__ == "__main__":

    # Start streaming data to ardyh.
    ardyh = ArdyhClient(protocols=['http-only', 'chat'])
    ardyh.connect()

    #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()