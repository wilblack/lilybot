"""
This is ardyh
Tornado Websockts server used the pass for lilybots.

Wil Black, wilblack21@gmail.com 
Oct. 26, 2013

"""
import time 

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

      print 'Received...', message        # prints the recived from the webpage 
      self.broadcast(message, 'echo')


    def on_close(self):
      print 'connection closed...'
      listeners.remove(self)
      self.broadcast("Closed %s" %(self.request.remote_ip))


    def broadcast(self, message, mode=None):
        for l in listeners:
            l.log(message, mode)



    def log(self, message, mode=None):
      now = dt.now().strftime(LOG_DTFORMAT)
      
      if mode == 'echo':
        message = message
      else:
        message = "[%s] ardyh: %s" %(now, message)
      

      print "Sending... ", message
      self.write_message(message)


    def loopCallback(self):
      now = dt.now().strftime(LOG_DTFORMAT)
      message = "[%s]" %(now)
      self.write_message(message)


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
  
