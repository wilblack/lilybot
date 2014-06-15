import sys
sys.path.append("/home/pi/projects/GrovePi/Software/Python")


from grovepi import *


class GrovePiSensorValues:
    
    sensors = [{'type':'temp',
                'default':0,
               },

               {'type':'humidity',
                'default':0,
               },

               {'type':'sound',
                'default':0,
               },

               {'type':'light',
                'default':0,
               },

               {'type':'slider',
                'default':0,
               },

               {'type':'touch',
                'default':0,
               },

               {'type':'pir',
                'default':0,
               },

               {'type':'dist',
                'default':0,
               },

               {'type':'acc_xyz',
                'default':[0,0,0],
               },

               ]

    def __init__(self):
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
            self.pir = digitalRead(4)
        except IOError:
            pass
        except ValueError:
            pass

        # This is the dht sensor
        try:
            self.temp, self.humidity = dht(4,1)
        except IOError:
            pass
        except ValueError:
            pass

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

        # out = {'temp':round(self.temp,2),
        #        'sound':self.sound,
        #        'light':self.light,
        #        'slider':self.slider,
        #        'button':self.button,
        #        'touch':self.touch}
        return out


grovePiSensorValues = GrovePiSensorValues()


class Grovebot(object):
    
    def __init__(self):
        self.commands = []








