"""
This module starts the ardyh client on a Raspberry Pi.

Written by Wil Black wilblack21@gmail.com Apr, 5 2014
"""

import json, urllib, sys, ast


from datetime import datetime as dt

from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop

import tornado
import tornado.web
import tornado.ioloop

from settings import *
from router import Router
from bot_roles.core import Core
from utils import get_mac_address


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

    def __init__(self, protocols, uri='ws://173.255.213.55:9093/ws'):
        rs = super(ArdyhClient, self).__init__(uri, protocols)
        

        self.ARDYH_URI = uri
        self.LOG_DTFORMAT = "%H:%M:%S"
        self.CTENOPHORE = CTENOPHORE
        

        # set the name to MAC address if not found.
        self.bot_name = settings['bot_name']
        self.bot_roles = settings['bot_roles']

        self.core = Core()
        self.router = Router()

    def opened(self):
        print "Connection to ardh is open"
        message = {'bot_name':self.bot_name, 
                   'bot_roles':self.bot_roles,
                   'mac':get_mac_address(),
                   'handshake':True}

        self.send(message)


    def received_message(self, message):
        self.router.received_message(message)


    def send(self, message):
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


if __name__ == "__main__":

    # Start streaming data to ardyh.
    ardyh = ArdyhClient(protocols=['http-only', 'chat'])
    ardyh.connect()
    #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()
    print "Could not open web socket connect to ardyh"
