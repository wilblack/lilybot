#Joshwa
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with Lego Motors & Lego Ultrasonic Sensor
# Make the connections with Left Motor at Port A, Right Motor at Port D and Sensor at Port 4
# Setup battery power source for the RPi & BrickPi and boot. 
# To control the program, connection must be made though SSH though PuTTY or similar software
# Open up PuTTY and enter UserName:pi Password:raspberry (Default values)
# Navigate to the directory containing this code and enter 'python Car.py'
# The user needs to enter one of the following keys:
# 8 - Forward
# 4 - Left
# 6 - Right
# 2 - Reverse
# 5 - Stop
# Also, The motors automatically stop when any nearby object is detected using the Ultrasonic Sensor
#
# This code has been modified from the original here https://github.com/DexterInd/BrickPi_Python
# Wil Black, wilblack21@gmail.com 
# Oct. 26, 2013
#
import os, json
from uuid import getnode as get_mac
import subprocess
from datetime import datetime as dt

from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop


from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template


LOG_DTFORMAT = "%H:%M:%S"

ARDYH_URI = 'ws://173.255.213.55:9093/ws'


def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def shutdown():
  command = "/usr/bin/sudo /sbin/shutdown -h now"
  process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  output = process.communicate()[0]
  print output


class MainHandler(tornado.web.RequestHandler):
  
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("www/index.html").generate())
c=0


class WSHandler(tornado.websocket.WebSocketHandler):
  
  def open(self):
    
    msg = "Hello, I'm lilybot%s" %s("WTF")
    print msg
    
    self.log(meg)
    sensors = tornado.ioloop.PeriodicCallback(self.get_sensors_values, 500)
    sensors.start()


  def get_sensors_values(self):

    out = [
        ['PORT_1', BrickPi.Sensor[PORT_1]],
        ['PORT_2', BrickPi.Sensor[PORT_2]],
        ['PORT_3', BrickPi.Sensor[PORT_3]],
        ['PORT_4', BrickPi.Sensor[PORT_4]],
      ]

    self.write_message({'sensor_values':out})


  def on_message(self, message):      # receives the data from the webpage and is stored in the variabe message
    # global c
    # print 'received:', message        # prints the recived from the webpage 
    # c = 0
    # if message == "u":                # checks for the received data and assigns different values to c whicch controls the movement of robot.
    #   c = "8";
    # if message == "d":
    #   c = "2"
    # if message == "l":
    #   c = "6"
    # if message == "r":
    #   c = "4"
    # if message == "b":
    #   c = "5"

    # Wil's added capabilites
    if message == "nl":
      self.log("Nudge Left")
      BrickPi.MotorSpeed[PORT_A] = 0  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
      time.sleep(.5)
      BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
      
    if message == "nr":
      self.log("Nudge Right")
      BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = 0  #Set the speed of MotorA (-255 to 255)
      time.sleep(.5)
      BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)

    if message == "x":  # Shutdown
      self.log("Shutting down")
      shutdown()
    if message == "y":  # Shutdown
      restart()

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
      self.log("Old Stopped")
      BrickPi.MotorSpeed[PORT_A] = 0
      BrickPi.MotorSpeed[PORT_D] = 0
    
    BrickPiUpdateValues()                # BrickPi updates the values for the motors
  

  def on_close(self):
    print 'connection closed...'
    #self.log('connection closed...')


  def log(self, message):
    now = dt.now().strftime(LOG_DTFORMAT)
    message = "[%s] %s" %(now, message)
    print message
    self.write_message(message)

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])


class Ardyh(TornadoWebSocketClient):
    """
    Web Socket client to connect to ardyh on start up.
    """

    def __init__(self, uri, protocols):
        rs = super(Ardyh, self).__init__(uri, protocols)
        self.bot = JJBot()
        self.LOOK_SPEED = 80
        self.LOOK_DT = 0.5

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




class JJBot():

    def __init__(self):
        self.source_path = "/tmp/stream/"


    def on_message(self, message):
        pass
    
    def get_sensors_values(self):
        out = [
            ['PORT_1', BrickPi.Sensor[PORT_1]],
            ['PORT_2', BrickPi.Sensor[PORT_2]],
            ['PORT_3', BrickPi.Sensor[PORT_3]],
            ['PORT_4', BrickPi.Sensor[PORT_4]],
          ]
        return out

    def startCamera(self):
        """

        mkdir /tmp/stream
        raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0
        LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/jjbot/www"

        """
        print "In JJBot.startCamera()"
        if not os.path.exists(self.source_path):
            os.mkdir(self.source_path)

        print "Calling raspistill command"
        command = "raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0"
        process1 = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        print process1
        

        # print "Calling mjpg_streamer command"
        # command = 'LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/jjbot/www"'
        # process2 = subprocess.Popen(command.split(), stdout=subprocess.PIPE)



    def stopCamera(self):
        pass



class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting thread %s" %(self.threadID)
        while running:
            result = BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            time.sleep(.2)              # sleep for 200 ms


if __name__ == "__main__":
    BrickPiSetup()  # setup the serial port for communication
    BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
    BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor A
    BrickPi.MotorEnable[PORT_C] = 1 #Enable the Motor D
    BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor D


    BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT   #Set the type of sensor at PORT_1
    BrickPiSetupSensors()   #Send the properties of sensors to BrickPi
    
    # Start the local webserver to listen for incoming requests.
    running = True
    thread1 = myThread(1, "Thread-1", 1)
    thread1.setDaemon(True)
    thread1.start()  
    application.listen(9010)

    # Start streaming data to ardyh.
    ardyh = Ardyh(ARDYH_URI, protocols=['http-only', 'chat'])
    ardyh.connect()

       #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()

