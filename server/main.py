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
import sys, json, ast
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
VERBOSE = True
PORT = 9093
LOG_DTFORMAT = "%H:%M:%S"
IP = "173.255.213.55"



listeners = []

def get_bot_listener(bot_name):
    return next( bot for bot in listeners if bot['bot_name'] == bot_name )



class MainHandler(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://ardyh.solalla.com")

    def get(self, action=None):
        """
        Displays the webpage.
        """
        if action == "bots-list":
            out = json.dumps([ {'bot_name':l['bot_name'], 'subscriptions':l['subscriptions']} for l in listeners])
            self.write(out)
        else:
            loader = tornado.template.Loader(".")
            self.write(loader.load("templates/index.html").generate())


class TwineHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://ardyh.solalla.com")

    def get(self, action):
        print "Got message ", action

        for bot in listeners:
            if action == "bottom":
              message = json.dumps({'command':'allOff', 
                                  'kwargs': {}})
            else:
              if action == "top":
                color = "#FF00FF"
              elif action == "back":
                color = "#0000FF"
              elif action == "front":
                color = "#00FFFF"
              elif action == "left":
                color = "#00FF00"
              elif action == "right":
                color = "#FF0000"
              elif action == "shake":
                color = "#FFFFFF"
              message = json.dumps({'command':'fillRGB', 
                                    'kwargs': {'color':color}
                                    })
            bot['socket'].write_message(message)
        self.write("Received action %s" %(action))


class WSHandler(tornado.websocket.WebSocketHandler):
    
    def __init__(self, uri, protocols):
        super(WSHandler, self).__init__(uri, protocols)

        self.nav = ArdyhNav(self)
        self.portA_fifo = collections.deque(5*[255], 5)
        self.busy = False # Tells the ardyh to stop sending messages to listener, useful while executing a command
        self.operationa_mode = "user_controlled"

    def open(self):
        print 'connection opened...'
        bot = {"socket":self,
                "subscriptions":[]}
        try:
            bot_name = self.request.uri.split("?")[1]
        except:
            bot_name = ""
        
        bot.update({"bot_name":bot_name})

        print "this is %s" %bot_name
        self.connected_to = bot_name
        listeners.append( bot )


    def on_message(self, message):      # receives the data from the webpage and is stored in the variabe message
        """
        Messages should come as a JSON Object string.

        """
        if VERBOSE: print "recieved message: \n", message
        try:
            messageObj = ast.literal_eval(message)
        except ValueError, e:
            try:
                messageObj = json.loads(message)
            except:
                print sys.exc_info()[0]
                if VERBOSE: print "Message is not JSON"
                return

        if 'handshake' in messageObj.keys():
            print "Updating %s's subscriptions to %s" %(messageObj['bot_name'], messageObj['subscriptions'])
            bot = get_bot_listener(messageObj['bot_name'])
            bot.update({'subscriptions':messageObj['subscriptions']})


        # if 'handshake' in messageObj.keys():
        #     pass
        # else:
        #     self.broadcast(messageObj)
        self.broadcast(messageObj)
    def on_close(self):
        print 'connection closed...'
        
        bot = next( bot for bot in listeners if bot['bot_name'] == self.connected_to )
        listeners.remove(bot)

        #self.broadcast("Closed %s" %(bot['bot_name']))


    def broadcast(self, message, mode=None):
        if 'channel' in message.keys():
            channel = message['channel']
        else:
            channel = ""

        # out = json.dumps(message)
        out = message
        # import pdb; pdb.set_trace()
        for sub in self.get_subscribers(channel):
            out.update({'from':sub['bot_name']})
            sub['socket'].write_message(out)

        
    def get_subscribers(self, channel):
        """

        Checks listeners for a bots with channel in their subscription list.
        channel is usaully a bot_name.

        Returns:
            If channel is falsy then the all listeners are returned else
            returns a lit of listerns.

        """
        if channel:
            return [bot for bot in listeners if channel in bot['subscriptions'] ]
        else:
            return listeners


    def log(self, message, mode=None):
      """
      if mode is None then turns on the ardyh signature

      """
      if VERBOSE: print "Message: \n", message
      if self.busy: return
      now = dt.now().strftime(LOG_DTFORMAT)
      if not mode == 'echo':
        message = "[%s] ardyh: %s" %(now, message)
      
      # Update with ardyh timestamp. 
      
      if message.__class__ == {}.__class__:
        if VERBOSE: print "message is a dict"
        message.update({"ardyh_timestamp":"%s" %(now)})
      else:
        if VERBOSE: print "message is a string"        
        message = {"message":message, "ardyh_timestamp": "%s" %(now) }


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
      (r'/(bots-list)', MainHandler),
      (r'/twine/(.*)', TwineHandler),
      (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
    ])


if __name__ == "__main__":
    
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT) 
    #application.listen(PORT)
    
    print "Starting server at %s:%s" %(IP, PORT)          #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()
  
