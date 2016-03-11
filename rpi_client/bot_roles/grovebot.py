import sys, traceback
from datetime import datetime as dt

from settings import SENSORS, ISO_FORMAT
from bot_roles.core import Core
# from lib import digital_light_sensor as dls
from lib import TSL2561 as tsl

sys.path.append("/home/pi/projects/GrovePi/Software/Python")
from grovepi import *


class GrovePiSensorValues:

    def __init__(self):
        self.sensors = SENSORS
        self.sensors_types = [sens['type'] for sens in SENSORS]
        tsl.init()

        for sensor in self.sensors:
            setattr(self, sensor['type'], sensor['default'])

    def update(self):
        """
        Updates all sensor values, making them available at 
        self.SENSOR_NAME

        """

        if 'sound' in self.sensors_types:
            try:
                self.sound = analogRead(1)
            except IOError:
                pass
            except ValueError:
                pass

        # This is the light sensor
        if 'light' in self.sensors_types:
            try:
                raw = analogRead(2)
            except IOError:
                pass
            except ValueError:
                pass
            if raw < 10000:
                self.light = raw
            else:
                self.light = None

        # This is the digital light sensor v1.1
        if 'lux' in self.sensors_types:
            self.lux = tsl.readVisibleLux()
            #print "Lux: %i [vis+ir=%i, ir=%i @ gain=%ix, timing=%.1fms]" % (self.lux, tsl.channel0, tsl.channel1, tsl.gain_m, tsl.timing_ms)
            self.channel0 = tsl.channel0
            self.channel1 = tsl.channel1
            self.gain_m = tsl.gain_m
            self.timing_ms = tsl.timing_ms

            #raw = dls.read()
            #self.lux = raw["lux"]


        # This is the slider switch sensor
        if 'slider' in self.sensors_types:
            try:
                self.slider = digitalRead(3)
            except IOError:
                pass
            except ValueError:
                pass

        # This is the button
        if 'button' in self.sensors_types:
            try:
                self.button = digitalRead(2)
            except IOError:
                pass
            except ValueError:
                pass

        # This is the touch sensor
        if 'touch' in self.sensors_types:
            try:
                self.touch = digitalRead(7)
            except IOError:
                pass
            except ValueError:
                pass

        # This is the pir sensor
        if 'pir' in self.sensors_types:
            try:
                self.pir = digitalRead(3)
            except IOError:
                pass
            except ValueError:
                pass
            except:
                print "Error in pir read."
                traceback.print_exc(file=sys.stdout)

        # This is the dht sensor port
        if 'temp' in self.sensors_types and 'humidity' in self.sensors_types:
            try:
                [self.temp, self.humidity] = dht(4, 1)
                #print "temp: %s, humidity %s" % (self.temp, self.humidity)
            except IOError:
                print "dht IOError"
            except ValueError:
                print "dht ValueError"


        # This is the acc_xyy Accelerometer sensor, use port I2C-1
        if 'acc_xyz' in self.sensors_types:
            try:
                self.acc_xyz = acc_xyz()
            except IOError:
                print "acc_xyz IOError"
            except ValueError:
                print "acc_xyz ValueError"

        # This is the acc_xyy Accelerometer sensor
        if 'dist' in self.sensors_types:
            try:
                self.dist = ultrasonicRead(8)
            except IOError:
                pass
            except ValueError:
                pass

    def toDict(self):
        out = {}
        for sensor in self.sensors:
            val = getattr(self, sensor['type'])
            out.update({sensor['type']: val})

        print out
        return out


grovePiSensorValues = GrovePiSensorValues()


class Grovebot(Core):
    """
    This is the cammand handler.

    """
    
    def __init__(self, socket):
        super(Grovebot, self).__init__(socket)
        self.commands.append('read_sensors')
        self.commands.append('set_sampling_frequency')

        self.sensors = grovePiSensorValues

    def read_sensors(self, kwargs=None):
        print "in read_sensors"
        sensor_values = self.sensors.toDict()
        timestamp = dt.now().strftime(ISO_FORMAT)
        sensor_values.update({
            'bot_package':'grovebot',
            'timestamp': timestamp

        })

        out = {"message": {"command":"sensor_values", "kwargs":sensor_values }}
        self.socket.send(out)

    def set_sampling_frequency(self, kwargs=None):
        print "In set set_sampling_frequency"
