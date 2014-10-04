import sys
from settings import SENSORS

sys.path.append("/home/pi/projects/GrovePi/Software/Python")



from grovepi import *


class GrovePiSensorValues:
    

    def __init__(self):
        self.sensors = SENSORS
        for sensor in self.sensors:
           setattr(self, sensor['type'], sensor['default'])

    def update(self):
        try:
            self.temp = temp(0)
        except IOError:
            print "--"
        except ValueError:
            print self.temp

        try:
            self.sound = analogRead(1)
        except IOError:
            pass
        except ValueError:
            pass

        # This is the light sensor
        try:
            self.light = analogRead(2)
        except IOError:
            pass
        except ValueError:
            pass

        # This is the slider switch sensor
        try:
            self.slider = digitalRead(3)
        except IOError:
            pass
        except ValueError:
            pass

        # # This is the button
        # try:
        #     self.button = digitalRead(2)
        # except IOError:
        #     pass
        # except ValueError:
        #     pass

        # This is the touch sensor
        try:
            self.touch = digitalRead(7)
        except IOError:
            pass
        except ValueError:
            pass

        # This is the pir sensor
        try:
            self.pir = digitalRead(3)
        except IOError:
            pass
        except ValueError:
            pass

        # This is the dht sensor port 
        try:
            print "dht reading"
            self.temp, self.humidity = digitalRead(4)
            
        except IOError:
            print "dht IOError"
        except ValueError:
            print "dht ValueError"

        # This is the acc_xyy Accelerometer sensor
        try:
            self.acc_xyz = acc_xyz()
        except IOError:
            pass
        except ValueError:
            pass

        # This is the acc_xyy Accelerometer sensor
        try:
            self.dist = ultrasonicRead(8)
        except IOError:
            pass
        except ValueError:
            pass


    def toDict(self):
        out= {}
        for sensor in self.sensors:
            val = getattr(self, sensor['type'])
            out.update({sensor['type']: val})

        print "toDict: ", out
        return out


grovePiSensorValues = GrovePiSensorValues()


class Grovebot(object):
    
    def __init__(self):
        self.commands = []








