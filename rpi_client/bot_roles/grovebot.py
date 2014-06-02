import sys
sys.path.append("/home/pi/projects/GrovePi/Software/Python")


from grovepi import *


class GrovePiSensorValues:
    temp = 0
    sound  = 0
    light = 0

    def update(self):
        try:
            self.temp = temp(0)
        except IOError:
            print "--"
        except ValueError:
            print self.temp

    def toDict(self):
        out = {'temp':self.temp,
               'sound':self.sound,
               'light':self.light}
        return out


grovePiSensorValues = GrovePiSensorValues()

