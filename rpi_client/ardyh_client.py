"""
This module starts the ardyh client on a Raspberry Pi.

Written by Wil Black wilblack21@gmail.com Apr, 5 2014
"""

import json, urllib, sys, ast
import threading

from datetime import datetime as dt

from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop

import tornado
import tornado.web
import tornado.ioloop

from settings import settings, URI, VERBOSE
from router import Router
from bot_roles.core import Core
from utils import get_mac_address

UPDATE_SENSOR_DT = 0.2
LOOP_CALLBACK_DT = 0.4

if "jjbot" in settings["bot_packages"]:
    from BrickPi import *   #import BrickPi.py file to use BrickPi operations
    

if 'grovebot' in settings["bot_packages"]:
    from bot_roles.grovebot import *


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

    def __init__(self, protocols, uri='ws://173.255.213.55:9093/ws?'):
        rs = super(ArdyhClient, self).__init__(uri, protocols)
        

        self.ARDYH_URI = uri
        self.LOG_DTFORMAT = "%H:%M:%S"
       
        self.channel = settings['bot_name']
        self.bot_name = settings['bot_name']
        self.bot_roles = settings['bot_roles']

        self.core = Core()
        self.router = Router()


    def opened(self):
        print "Connection to ardh is open"
        message = {'bot_name':self.bot_name, 
                   'bot_roles':self.bot_roles,
                   'mac':get_mac_address(),
                   'handshake':True,
                   'subscriptions':settings['subscriptions']
                   }


        self.send(message)

        if ["jjbot", "grovebot"] and settings["bot_packages"]:
            print "Registering IO Loop callback"
            sensors = tornado.ioloop.PeriodicCallback(self.loopCallback, LOOP_CALLBACK_DT*1000)
            sensors.start()


    def received_message(self, message):
        self.router.received_message(message)

    def send(self, message):
        """
        Message should be of the form {MESSAGE_OBJ}
        

        - message
        -- bot_name
        -- from
        -- message
        -- command
        -- channel 
        -- ardyh_timestamp - May not be present

        """
        if VERBOSE: print "[ArdyhClient.send] Trying to send message:\n\n%s" %(message) 
        channel = settings['bot_name']
        message.update({
            "bot_name":self.bot_name,
            "channel":self.channel
        })
        message = json.dumps(message)
        
        if VERBOSE: print "[ArdyhClient.send] Send message:\n\n%s" %(message) 
        try:
            super(ArdyhClient, self).send(message)
        except:
            print "[ERROR] Message not send() failed."
            print sys.exc_info()[0]

    def closed(self, code, reason=None):
        print "Closed down", code, reason
        
        ioloop.IOLoop.instance().stop()
        #ioloop.IOLoop.instance().start()

    def log(self, message):
        now = dt.now().strftime(self.LOG_DTFORMAT)
        message = "[%s] %s" %(now, message)
        print message
        #self.send(message)


    def loopCallback(self):
        out = {}
        if "jjbot" in settings["bot_packages"]:
            sensor_values = self.get_sensors_values('jjbot') # This is where to sensor values get sent to ardyh
            out = {"message": {"sensor_values":sensor_values, "sensor_package":"jjbot"} }

        if "grovebot" in settings["bot_packages"]:
            sensor_values = self.get_sensors_values('grovebot') # This is where to sensor values get sent to ardyh
            out = {"message": {"sensor_values":sensor_values, "sensor_package":"grovebot"} }

        if out: self.send(out)


    def get_sensors_values(self, bot_package):
        if bot_package == 'jjbot':
            out = [
                ['PORT_1', BrickPi.Sensor[PORT_1]],
                ['PORT_2', BrickPi.Sensor[PORT_2]],
                ['PORT_3', BrickPi.Sensor[PORT_3]],
                ['PORT_4', BrickPi.Sensor[PORT_4]],
              ]
        if bot_package == 'grovebot':
            out = grovePiSensorValues.toDict()
        return out

if ["jjbot", "grovebot"] and settings["bot_packages"]:

    class SensorThread (threading.Thread):
        """
        I think this just tells the BrickPi to update the values, their is no networking involved.

        """
        def __init__(self, threadID, name):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
        def run(self):
            print "Starting thread %s" %(self.threadID)
            while sensor_thread_running:
                if 'jjbot' in settings['bot_packages']:
                    result = BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
                if 'grovebot' in settings['bot_packages']:
                    grovePiSensorValues.update()

                time.sleep(UPDATE_SENSOR_DT)



if __name__ == "__main__":
    
    sensor_thread_running = True # This is a gloable, should probably be on a per sensor basis.

    if "jjbot" in settings["bot_packages"]:
        BrickPiSetup()  # setup the serial port for communication
        BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
        BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor A
        BrickPi.MotorEnable[PORT_C] = 1 #Enable the Motor D
        BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor D

        BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT   #Set the type of sensor at PORT_1
        BrickPiSetupSensors()   #Send the properties of sensors to BrickPi
        
        thread1 = SensorThread(1, "Thread-1")
        thread1.setDaemon(True)
        print "Starting BrickPi sensors"
        thread1.start()

    if "grovebot" in settings["bot_packages"]:
        
        grovebot_thread = SensorThread(2, 'Grovebot Thread')
        grovebot_thread.setDaemon(True)
        print "Starting GroveBot sensors"
        grovebot_thread.start()


    # Start streaming data to ardyh.
    ardyh = ArdyhClient(uri=URI, protocols=['http-only', 'chat'])
    ardyh.connect()
    #starts the websockets connection
    print "Starting ioLoop"
    tornado.ioloop.IOLoop.instance().start()
    print "Could not open web socket connect to ardyh"


