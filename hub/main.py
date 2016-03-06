"""
This is ardyh
Tornado Websockts server used the pass for lilybots.

Wil Black, wilblack21@gmail.com 
Oct. 26, 2013



## Messages

- message
    -- name
    -- from
    -- message
    -- command
    -- channel
    -- ardyh_timestamp - May not be present


"""
import sys, json, ast, math, os
import time 
import collections
import datetime
from datetime import datetime as dt

import paho.mqtt.client as mqtt

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

from sensor_db import Db
db = Db()

# Settings
VERBOSE = True
PORT = 9093
LOG_DTFORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
IP = "192.168.0.105"
ARDYH_MONITOR = 'monitor.solalla.ardyh'

MQTT_BROKER_URL = "192.168.0.105"
PATH = os.path.dirname(os.path.abspath(__file__))



def start_mqtt_cient(socket):

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        bot_topics = [
            ("ardyh/bots/rpi1", 0),
            ("ardyh/bots/rpi2", 0),
            ("ardyh/bots/rpi3", 0),
            ("ardyh/bots/rpi4", 0)
        ]
        client.subscribe(bot_topics)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        
        # send messages over web socket
        socket.write_message({"topic": msg.topic, "payload": json.loads(msg.payload)})

        # log message data to rrd
        db.update(msg.topic, msg.payload['temp'] )

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_URL, 1883, 60)

    print "Starting mqtt client"
    client.loop_start()
    return client


class HubWebRequestHandler(tornado.web.RequestHandler):

    def set_allow_origin(self, request):
        origin_domain = self.request.headers.get("Origin", None)

        if origin_domain:
            self.set_header("Access-Control-Allow-Origin", origin_domain)
        else:
            self.set_header("Access-Control-Allow-Origin", "*")

class MainHandler(HubWebRequestHandler):

    # def set_default_headers(self):
    #     self.set_header("Access-Control-Allow-Origin", "http://ardyh.solalla.com")
    #     self.set_header("Access-Control-Allow-Origin", "http://ctenophore.solalla.com")

    def get(self, action=None):
        """
        Displays the webpage.
        """
        self.set_allow_origin(self.request)

        if action == "bots-list":
            # out = [ {'bot_name':l['bot_name'], 'subscriptions':l['subscriptions']} for l in listeners]
            temp = []
            for l in listeners:
                row = {
                    'bot_name': l['bot_name'],
                    'bot_roles': l['bot_roles'],
                    'mac': l.get('mac', ''),
                    'local_ip': l.get('local_ip', ''),
                    'subscriptions': l.get('subscriptions', ''),
                    'sensors': l.get('sensors', []),
                }
                temp.append(row)

            out = json.dumps(temp)
            self.write(out)
        else:
            loader = tornado.template.Loader(".")
            self.write(loader.load("templates/index.html").generate())




class WSHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(WSHandler, self).__init__(application, request, **kwargs)

        # Start listening to rpi here
        self.mqtt = start_mqtt_cient(self)

    def check_origin(self, origin):
        return True

    def open(self):
        print "Connection opened..."
        print 'Sucessfully established socket connection'



    def on_message(self, message):
        """
        Tries to forward commands to the appropruate mqtt channel (botName).

        This receives messages as strings. message is then loaded into python.
        It will look for a keyword named "command" in the message object.

        If it has a command, it will look for a 'botName', in kwargs. The botName should
        be the mqtt channel and it will be used to publish an object containing
        the a command, kwargs key/val pairs. These should be picked up in rpi_client.



        """
        # print "[WSHandler.on_message] message ", message
        # Need to catch these and route the to the apropriate mqtt channel.
        message = json.loads(message);
        if 'command' in message.keys():
            cmd = message['command']
            kwargs = message['kwargs']
            channel = kwargs.get('botName', None)
            if channel:
                payload = {
                    'command': cmd,
                    'kwargs': kwargs
                }
                self.mqtt.publish(channel, json.dumps(payload))

        #channel = message.botName
        #payload = message.data
        #



    def on_close(self):
        print 'Lost a %s. connection closed.'




application = tornado.web.Application([
      (r'/ws', WSHandler),
      #(r'/', MainHandler),
      (r'/(bots-list)', MainHandler),
      (r"/(.*)", tornado.web.StaticFileHandler, {'path':os.path.join(PATH, 'homeMonitor/dist')}),
    ])


if __name__ == "__main__":
    #r = redis.StrictRedis(host='localhost', port=6379, db=0)

    print "Starting HTTP server at %s:%s" %(IP, PORT) 
    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(PORT) 
    application.listen(PORT)
    
    print "Starting Websocket server at ws://%s:%s" %(IP, PORT)          #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()
  
