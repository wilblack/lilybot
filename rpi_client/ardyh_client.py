"""
This module starts the ardyh client on a Raspberry Pi.

Written by Wil Black wilblack21@gmail.com Apr, 5 2014
"""

import json, urllib, sys, ast
from time import sleep

from datetime import datetime as dt

from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop

import tornado
import tornado.web
import tornado.ioloop

from settings import *
from utils import get_mac_address, shutdown, restart
from router import Router



# class MainHandler(tornado.web.RequestHandler):
  
#   def get(self):
#     loader = tornado.template.Loader(".")
#     tv = settings.settings
#     self.write(loader.load("../../web_client/monitor.html").generate(settings=tv))



class ArdyhClient(TornadoWebSocketClient):
    """
    Web Socket client to connect to ardyh on start up.
    
    Data is passed back and forth using a message object. 
    the message object is a JSON Object with the following keywords

    - message
    -- name
    -- from
    -- message
    -- command
    -- ardyh_timestamp - May not be present

    """

    def __init__(self, protocols, uri='ws://173.255.213.55:9093/ws'):
        rs = super(ArdyhClient, self).__init__(uri, protocols)
        

        self.ARDYH_URI = uri
        self.LOG_DTFORMAT = "%H:%M:%S"
        self.CTENOPHORE = CTENOPHORE
        self.core_commands = ['shutdown', 'restart']

        

        # set the name to MAC address if not found.
        self.bot_name = settings['bot_name']
        self.bot_roles = settings['bot_roles']
        self.mac = get_mac_address()

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

        # Initialize router
        config = {"JJBOT":self.JJBOT,
                  "CTENOPHORE":self.CTENOPHORE
                  }
        self.router = Router(config)


    def opened(self):
        print "Connection to ardh is open"
        message = {'bot_name':self.bot_name, 
                   'bot_roles':self.bot_roles,
                   'mac':self.mac,
                   'handshake':True}

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
        self.router.received_message(message)


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

    def refresh_connection(){

    }

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


    

    def hex2rgb(self, hex):
        return [ord(c) for c in hex[1:].decode("hex")]



    def receive_core_command(self, cmd, kwargs):
        

        


# application = tornado.web.Application([
#  #(r'/ws', WSHandler),
#   (r'/', MainHandler),
  
#   (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./www/static"}),
# ])


if __name__ == "__main__":
    # # Start the web application
    # HTTP_PORT = 9010
    # print "Starting web application on port %s" %(HTTP_PORT)
    # application.listen(HTTP_PORT)

    # Start streaming data to ardyh.
    ardyh = ArdyhClient(protocols=['http-only', 'chat'])
    ardyh.connect()
    #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()
    print "Could not open web socket connect to ardyh"
