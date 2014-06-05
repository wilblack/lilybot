import sys
sys.path.append("/home/pi/projects/GrovePi/Software/Python")


from grovepi import *


class GrovePiSensorValues:
    temp = 0
    sound  = 0
    light = 0
    slider = 0
    button = 0
    touch = 0

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

        # This is the button
        try:
            self.button = digitalRead(2)
        except IOError:
            pass
        except ValueError:
            pass

        # This is the touch sensor
        try:
            self.touch = digitalRead(7)
        except IOError:
            pass
        except ValueError:
            pass


    def toDict(self):
        out = {'temp':round(self.temp,2),
               'sound':self.sound,
               'light':self.light,
               'slider':self.slider,
               'button':self.button,
               'touch':self.touch}
        return out


grovePiSensorValues = GrovePiSensorValues()


class Grovebot(object):
    
    def __init__(self):
        self.commands = []








