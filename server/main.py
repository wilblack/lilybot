"""
This is ardyh
Tornado Websockts server used the pass for lilybots.

Wil Black, wilblack21@gmail.com 
Oct. 26, 2013

"""
import json
import time 
import collections

import datetime
from datetime import datetime as dt

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

# Settings
PORT = 9093
LOG_DTFORMAT = "%H:%M:%S"
IP = "173.255.213.55"

class MainHandler(tornado.web.RequestHandler):
  
    def get(self):
      """
      Displays the webpage.
      """
      loader = tornado.template.Loader(".")
      self.write(loader.load("templates/index.html").generate())


listeners = []

class WSHandler(tornado.websocket.WebSocketHandler):
    
    def __init__(self, uri, protocols):
      super(WSHandler, self).__init__(uri, protocols)


      self.nav = ArdyhNav(self)
      self.portA_fifo = collections.deque(5*[255], 5)
      self.busy = False # Tells the ardyh to stop sending messages to listener, useful while executing a command
      self.operationa_mode = "user_controlled"

    def open(self):
      print 'connection opened...'
      self.log('Hello, good to see you again.')
      listeners.append(self)
      self.broadcast("New connection: %s" %(self.request.remote_ip))


      #sensors = tornado.ioloop.PeriodicCallback(self.loopCallback, 5*1000)
      #sensors.start()


    def on_message(self, message):      # receives the data from the webpage and is stored in the variabe message
        """
        Messages should come with a unique ID. 

        lilybots should use MAC Address

        {"id":"AA:BB:CC:FF:EE"
        "message":MESSAGE TEXT
        }
        """

        message_json = None
        try:
            message_json = json.loads(message)
            # Append IP address to allow camera feed. 
            if "new" in message_json.keys():
                port = message_json['camera_port']
                message_json.update({"camera_url":"http://%s:%s" %(self.request.remote_ip, port) })
        except:
            pass

        

        self.broadcast(message, 'echo')
        
        if self.operationa_mode == "autonamous":
            if message_json:
                message = message_json
            else:
                return

            if "sensor_values" in message.keys():
                valueA = message['sensor_values'][0][1]
                self.portA_fifo.appendleft(valueA)

            
            if len([1 for val in self.portA_fifo if val < 35 ]) >= 3:
                print self.busy
                if not self.busy:
                    self.busy = True
                    self.nav.event('bump')



    def on_close(self):
      print 'connection closed...'
      listeners.remove(self)
      self.broadcast("Closed %s" %(self.request.remote_ip))


    def broadcast(self, message, mode=None):
        for l in listeners:
            l.log(message, mode)



    def log(self, message, mode=None):
      """
      if mode is None then turns on the ardyh signature

      """
      if self.busy: return
      now = dt.now().strftime(LOG_DTFORMAT)
      if mode == 'echo':
        message = message
      else:
        message = "[%s] ardyh: %s" %(now, message)
      
      if not message.__class__ == {}.__class__:
        message = {"message":message}
      
      message = json.dump(message)
      self.write_message(message)


    def loopCallback(self):
      now = dt.now().strftime(LOG_DTFORMAT)
      message = "[%s]" %(now)
      self.write_message(message)



class ArdyhNav():

    def __init__(self, conn):
        self.conn = conn

    def event(self, event_type):
        if event_type == 'bump':
            self.conn.write_message("d")
            tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=0.3), self.stop)
            tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1.0), self.rotateLeft)
            tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1.3), self.stop)
            tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1.4), self.tryForward)

    def stop(self):
        self.conn.write_message("b")

    def rotateLeft(self):
        self.conn.write_message("l")

    def rotateRight(self):
        self.conn.write_message("r")

    def tryForward(self):
        if self.conn.portA_fifo[1] >= 50:
            self.conn.write_message("u")
        print "trying to set self.conn.busy %s" %self.conn.busy
        self.conn.busy = False
        



application = tornado.web.Application([
      (r'/ws', WSHandler),
      (r'/', MainHandler),
      (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
    ])


if __name__ == "__main__":
    
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT) 
    #application.listen(PORT)
    
    print "Starting server at %s:%s" %(IP, PORT)          #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()
  
