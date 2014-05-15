import sys
from time import sleep

from settings import *
from utils import hex2rgb

try:
    print "Loading RPi-LPD8806"
    from raspledstrip.ledstrip import *
except SystemExit:
    print "[WARNING] RPi-LPD8806 bootstrap module found but no LEDS connected. Starting client anyways"
    print sys.exc_info()[0]

except:
    print "[WARNING] RPi-LPD8806 bootstrap module not found"
    print sys.exc_info()[0]



class Ctenophore(object):
    
    def __init__(self):

        self.commands = ['setRGB', 'target', 'allOff' ]

        # Initialize Lights, this does not belong here.
        self.NLEDS = NLEDS
        self.ALL_STOP = False
        self.led = LEDStrip(self.NLEDS)
        self.led.all_off()

        if VERBOSE: print "Initializing %s LEDS" %(self.NLEDS)
        
        for i in range(0, self.NLEDS):
            self.led.setRGB(i, 0,0,255)
            self.led.setRGB(self.NLEDS - i, 0, 255, 0)
            self.led.update()
            sleep(0.02)
            self.led.all_off()

    def setMode(self, kwargs):
        pass

    def setRGB(self, kwargs):
        r, g, b = hex2rgb(kwargs["color"])
        if VERBOSE: print "calling setRGB(%s,%s,%s,%s)" %(kwargs["index"], r, g, b)

        self.led.setRGB(kwargs["index"], r, g, b)
        self.led.update()

    def setOff(self, kwargs):
            if VERBOSE: print "called setOff()"

    def fillRGB(self, kwargs):
            r, g, b = self.hex2rgb(kwargs["color"])
            if VERBOSE: print "called fillRGB()"

    def fillOff(self, kwargs):
            if VERBOSE: print "called fillOff()"

    def allOff(self, kwargs):
            self.led.all_off()

    def target(self, kwargs):
        print "[Ctenophore.taget]"
        self.led.all_off()
        nrepeat = 4
        dt = 0.2
        width = 5 # Total length will be 2 8 width + 1
        index = int(kwargs["index"])

        for j in range(nrepeat):
            
            for i in range(width, 0, -1):
                lefti = index - i
                righti = index + i

                if righti < self.NLEDS-1:
                    self.led.setRGB(righti, 255,  0, 0)
                if lefti > 0:
                    self.led.setRGB(lefti, 255,  0, 0)
                self.led.update()
                sleep(dt)
        
            self.led.all_off()


    def clearTarget(self, kwargs):
        self.ALL_STOP = False
        self.all_off()

         # elif cmd == "animWave":
        #     anim = Wave(led, Color(255, 0, 0), 4)
        #     for i in range(led.lastIndex):
        #         anim.step()
        #         led.update()
        #     led.fillOff()
        #     led.update()
        #     self.log("Wave done")

        # elif cmd == "animRainbow":
        #     anim = Rainbow(led)
        #     for i in range(384):
        #         anim.step()
        #         led.update()
        #     led.fillOff()
        #     led.update()
        #     self.log("Rainbow done")