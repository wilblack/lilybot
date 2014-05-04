"""
This module starts the ardyh client on a Raspberry Pi.

Written by Wil Black wilblack21@gmail.com Apr, 5 2014
"""

import json, urllib, sys, ast
from time import sleep

from datetime import datetime as dt
from uuid import getnode as get_mac
from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop

import tornado.ioloop

try:
    print "Loading RPi-LPD8806"
    from raspledstrip.ledstrip import *
    CTENOPHORE = True
except SystemExit:
    print "[WARNING] RPi-LPD8806 bootstrap module found but no LEDS connected. Starting client anyways"
    print sys.exc_info()[0]
    CTENOPHORE = True

except:
    print "[WARNING] RPi-LPD8806 bootstrap module not found"
    print sys.exc_info()[0]
    CTENOPHORE = True


VERBOSE = True

class ArdyhClient(TornadoWebSocketClient):
    """
    Web Socket client to connect to ardyh on start up.
    
    Data is passed back and forth using a message object. 
    the message object is a JSON Object with the following keywords

    - message
    -- name
    -- from
    -- channel 
    -- message
    -- command
    -- ardyh_timestamp - May not be present

    """

    def __init__(self, protocols, name=None, uri='ws://173.255.213.55:9093/ws'):
        rs = super(ArdyhClient, self).__init__(uri, protocols)
        
        self.ARDYH_URI = uri
        self.LOG_DTFORMAT = "%H:%M:%S"
        self.CTENOPHORE = CTENOPHORE
        if self.CTENOPHORE:
            self.NLEDS = 64
            self.led = LEDStrip(self.NLEDS)
            self.led.all_off()

            if VERBOSE: print "Initializing %s LEDS" %(self.NLEDS)
            for i in range(0, self.NLEDS):
                self.led.setRGB(i, 0,0,255)
                self.led.setRGB(self.NLEDS - i, 0, 255, 0)
                self.led.update()
                sleep(0.05)
                self.led.all_off()

        # set the name to MAC address if not found.
        self.name = name or self.get_mac_address()

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
        message = {'name':self.name, 'type':'bot'}

        self.send(message)

        if self.JJBOT:
            try:
                "Trying to start sensors"
                sensors = tornado.ioloop.PeriodicCallback(self.loopCallback, 500)
                sensors.start()
            except:
                "[WARNING] Sensors not started"

            # Tells ardyh that is a new connection
            out = {"new":"", "camera_port":8080}
            self.send(out)
        




    def received_message(self, message):
        if VERBOSE: print "Received message: %s" %(message)

        try:
            message = ast.literal_eval(message.data)
        except:
            print sys.exc_info()[0]

        if self.JJBOT:
            self.receive_message_jjbot(message)

        elif self.CTENOPHORE:
            self.receive_message_ctenophore(message)

    def send(self, message):
        message = json.dumps(message)
        if VERBOSE: print "About to send message:\n\n%s" %(message) 
        try:
            super(ArdyhClient, self).send(message)
        except:
            print "[ERROR] Message not send() failed."
            print sys.exc_info()[0]

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

    def hex2rgb(self, hex):
        return [ord(c) for c in hex[1:].decode("hex")]

    def receive_message_ctenophore(self, message):
        if VERBOSE: print "this is a ctenophore message"
        if not "command" in message.keys(): 
            print "command not found in message"
            return


        cmd = message['command']
        kwargs = message.get('kwargs', {})
        if VERBOSE: print "command: %s\n" %(cmd), kwargs

        if cmd == "setMode":
            if VERBOSE: print "called setMode()"

        elif cmd == "setRGB":
            
            r,g,b = self.hex2rgb(kwargs["color"])
            if VERBOSE: print "calling setRGB(%s,%s,%s,%s)" %(kwargs["index"], r, g, b)
            self.led.setRGB(kwargs["index"], r, g, b)
            self.led.update()


        elif cmd == "setOff":
            if VERBOSE: print "called setOff()"

        elif cmd == "fillRGB":
            r,g,b = self.hex2rgb(kwargs["color"])
            if VERBOSE: print "called fillRGB()"

        elif cmd == "fillOff":
            if VERBOSE: print "called fillOff()"

        elif cmd == "allOff":
            if VERBOSE: print "called allOff()"

        # elif cmd == "animWave":
        #     anim = Wave(led, Color(255, 0, 0), 4)
        #     for i in range(led.lastIndex):
        #         anim.step()
        #         led.update()
        #     led.fillOff()
        #     led.update()
        #     self.log("Wave done")

        # elif cmd == "animRainbow":
        #     anim = Rainbow(led)
        #     for i in range(384):
        #         anim.step()
        #         led.update()
        #     led.fillOff()
        #     led.update()
        #     self.log("Rainbow done")


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
    ardyh = ArdyhClient(name="ctenopore", protocols=['http-only', 'chat'])
    ardyh.connect()

    #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()