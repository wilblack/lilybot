
from time import sleep
from bootstrap import *



class Ctenophore(object):
    
    def __init__():

        # Initialize Lights, this does not belong here.
        self.NLEDS = NLEDS
        self.led = LEDStrip(self.NLEDS)
        self.led.all_off()

        if VERBOSE: print "Initializing %s LEDS" %(self.NLEDS)
        for i in range(0, self.NLEDS):
            self.led.setRGB(i, 0,0,255)
            self.led.setRGB(self.NLEDS - i, 0, 255, 0)
            self.led.update()
            sleep(0.05)
            self.led.all_off()