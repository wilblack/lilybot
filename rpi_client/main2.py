"""


"""

from settings import settings, URI, VERBOSE, SENSORS, UPDATE_SENSOR_DT, LOOP_CALLBACK_DT
from router import Router
from bot_roles.core import Core
from utils import get_mac_address

import paho.mqtt.client as mqtt

MY_CHANNEL = "ardyh/bots/rpi3"


class ArdyClient(object):
    def __init__(self):
    self.conn = mqtt.Client()
    self.conn.on_connect = on_connect
    self.conn.on_message = on_message

    self.conn.connect("192.168.0.105", 1883, 60)
    client.loop_forever()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        
        self.conn.subscribe("ardyh/bots/rpi5")
        self.send_handshake()


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))


    def send_handshake(self):
            local_ip = commands.getoutput("hostname -I")

            message = {
                'bot_name': self.bot_name,
                'bot_roles': self.bot_roles,
                'mac': get_mac_address(),
                'handshake': True,
                'subscriptions': settings['subscriptions'],
                'sensors': SENSORS,
                'local_ip': local_ip
            }
            print "Sending handshake"
            self.send(message)

    def send(message, channel=MY_CHANNEL):
        timestamp = now = dt.now().strftime(self.LOG_DTFORMAT)
        message.update({
            "bot_name":self.bot_name,
            "timestamp": timestamp
        })

        message = json.dumps(message)
        self.conn.publish(channel, message)






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

    ardyh = ArdyhClient()
    







    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
