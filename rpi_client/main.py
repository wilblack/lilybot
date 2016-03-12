"""


"""
import threading, commands, json
import time
from datetime import datetime as dt

from settings import URI, VERBOSE, SENSORS, UPDATE_SENSOR_DT, \
                     LOOP_CALLBACK_DT, \
                     BOT_SUBSCRIPTIONS, BOT_CHANNEL, BOT_ROLES, BOT_NAME, BOT_PACKAGES, \
                     LOG_DTFORMAT, SENSOR_PUBLISH_DT
from router import Router
from bot_roles.core import Core
from utils import get_mac_address

import paho.mqtt.client as mqtt

MY_CHANNEL = "ardyh/bots/rpi3"

if "jjbot" in BOT_PACKAGES:
    from BrickPi import *   #import BrickPi.py file to use BrickPi operations


if 'grovebot' in BOT_PACKAGES:
    from bot_roles.grovebot import grovePiSensorValues


class ArdyhClient(object):
    
    def __init__(self):
        self.bot_channel = BOT_CHANNEL
        self.bot_roles = BOT_ROLES
        self.bot_subs = BOT_SUBSCRIPTIONS
        self.LOG_DTFORMAT = LOG_DTFORMAT

        self.conn = mqtt.Client()
        self.conn.on_connect = self.on_connect
        self.conn.on_message = self.on_message

        self.conn.connect("192.168.0.105", 1883, 60)
        

        self.conn.loop_start()
        router = Router(self)

        count = 0
        while True:
            out = self.get_sensors_values('grovebot')
            self.send(out)
            time.sleep(SENSOR_PUBLISH_DT)


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        self.conn.subscribe("ardyh/bots/rpi5")
        self.send_handshake()


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))


    def send_handshake(self):
            local_ip = commands.getoutput("hostname -I")

            message = {
                'bot_channel':self.bot_channel,
                'bot_name': BOT_NAME,
                'bot_roles': self.bot_roles,
                'mac': get_mac_address(),
                'handshake': True,
                'subscriptions': BOT_SUBSCRIPTIONS,
                'sensors': SENSORS,
                'local_ip': local_ip
            }
            self.send(message)

    def send(self, message, channel=BOT_CHANNEL):
        timestamp = now = dt.now().strftime(self.LOG_DTFORMAT)
        message.update({
            "timestamp": timestamp
        })

        message = json.dumps(message)
        self.conn.publish(channel, message)


    def get_sensors_values(self, bot_package):
        """
        Returns a dict with sensors values.

        """

        if bot_package == 'jjbot':
            out = {
                'PORT_1': BrickPi.Sensor[PORT_1],
                'PORT_2': BrickPi.Sensor[PORT_2],
                'PORT_3': BrickPi.Sensor[PORT_3],
                'PORT_4': BrickPi.Sensor[PORT_4],
            }
        if bot_package == 'grovebot':
            out = grovePiSensorValues.toDict()
        return out




class SensorThread (threading.Thread):
    """
    I think this just tells the BrickPi to update the values, their is no networking involved.

    """
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stoprequest = threading.Event()

    def run(self):
        print "Starting thread %s" %(self.threadID)
        while not self.stoprequest.isSet():
            if 'jjbot' in BOT_PACKAGES:
                result = BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            if 'grovebot' in BOT_PACKAGES:
                grovePiSensorValues.update()

            time.sleep(UPDATE_SENSOR_DT)

        if self.stoprequest.isSet():
            print "******** STOP IT ************"


if __name__ == "__main__":
    

    if "jjbot" in BOT_PACKAGES:
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

    if "grovebot" in BOT_PACKAGES:
        grovebot_thread = SensorThread(2, 'Grovebot Thread')
        grovebot_thread.setDaemon(True)
        print "Starting GroveBot sensors"
        grovebot_thread.start()

    ardyh = ArdyhClient()









    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
