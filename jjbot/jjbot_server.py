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

import subprocess
from datetime import datetime as dt


from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template


LOG_DTFORMAT = "%m-%d %H:%M:%S"




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
    self.write(loader.load("index.html").generate())
c=0


class WSHandler(tornado.websocket.WebSocketHandler):
  
  def open(self):
    print 'connection opened...'
    self.log('connection opened...')

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
    global c
    print 'received:', message        # prints the recived from the webpage 
    c = 0
    if message == "u":                # checks for the received data and assigns different values to c whicch controls the movement of robot.
      c = "8";
    if message == "d":
      c = "2"
    if message == "l":
      c = "6"
    if message == "r":
      c = "4"
    if message == "b":
      c = "5"

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

    print c
    if c == '8' :
      self.log("Running Forward")
      BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
    elif c == '2' :
      self.log("Running Reverse")
      
      BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
    elif c == '4' :
      self.log("Turning Right")

      BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
    elif c == '6' :
      self.log("Turning Left")
      BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
      BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
    elif c == '5' :
      self.log("Stopped")
      BrickPi.MotorSpeed[PORT_A] = 0

      BrickPi.MotorSpeed[PORT_D] = 0
    BrickPiUpdateValues();                # BrickPi updates the values for the motors
    print "Values Updated"
  

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
  BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor D

  BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT   #Set the type of sensor at PORT_1

  BrickPiSetupSensors()   #Send the properties of sensors to BrickPi
  running = True
  thread1 = myThread(1, "Thread-1", 1)
  thread1.setDaemon(True)
  thread1.start()  
  application.listen(9093)          #starts the websockets connection
  tornado.ioloop.IOLoop.instance().start()
  
