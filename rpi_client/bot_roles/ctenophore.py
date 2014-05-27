import sys, time
import threading, Queue

from random import randint
from time import sleep
from math import floor

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

PULSE_DT = 10



class PassiveThread (threading.Thread):
    """
    
    """
    def __init__(self, name, ctenophore, output_queue):
        super(PassiveThread, self).__init__()
        
        self.name = name
        self.ctenophore = ctenophore
        self.output_queue  = output_queue
        self.stoprequest = threading.Event()

    def run(self):
        print "Starting thread %s" %(self.name)
        while not self.stoprequest.isSet():
            #self.ctenophore.fillRGB({"color":"#22FF33"})
            color = ('#%06X' % randint(0,256**3-1))
            self.ctenophore.pulse({"color":color})

            PULSE_DT = randint(12, 24)
            time.sleep(PULSE_DT)              # sleep for 200 ms


    def join(self, timeout=None):
        self.stoprequest.set() # Turns off the thread if it already started
        super(WorkerThread, self).join(timeout)


class Ctenophore(object):
    
    def __init__(self):

        self.commands = ['setRGB', 'fillRGB', 'target', 'allOff' ]

        # Initialize Lights, this does not belong here.
        self.NLEDS = NLEDS
        self.ALL_STOP = False
        self.led = LEDStrip(self.NLEDS)
        self.led.all_off()
        self.history = [255, 255, 255]
        if VERBOSE: print "Initializing %s LEDS" %(self.NLEDS)
        
        for i in range(0, self.NLEDS):
            self.led.setRGB(i, 0,0,255)
            self.led.setRGB(self.NLEDS - i, 0, 255, 0)
            self.led.update()
            sleep(0.01)
            self.led.all_off()


        # Create a single input and a single output queue for all threads.
        input_queue = Queue.Queue()
        output_queue = Queue.Queue()
        # Start passive thread
        self.passiveThread = PassiveThread("Passive Thread", self, output_queue)
        #self.passiveThread.setDaemon(True)
        self.passiveThread.start()

        


    def setMode(self, kwargs):
        pass

    def setRGB(self, kwargs):
        r, g, b = hex2rgb(kwargs["color"])
        self.led.setRGB(kwargs["index"], r, g, b)
        self.led.update()

    def setOff(self, kwargs):
        self.led.setOff(kwargs['index'])
        self.led.update()


    def fillRGB(self, kwargs):
        self.led.all_off()
        r, g, b = hex2rgb(kwargs["color"])
        start = kwargs.get("start", 0)
        end = kwargs.get("end", self.NLEDS)
        self.led.fillRGB(r, g, b, start, end)
        self.led.update()


    def fillOff(self, kwargs):
        if VERBOSE: print "called fillOff()"


    def allOff(self, kwargs):
            self.led.all_off()


    def target(self, kwargs):
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

    def pulse(self, kwargs):
        DT = 0.005
        color = kwargs['color']
        direction = kwargs.get('direction', None)

        for i in range(self.NLEDS):
            self.setRGB({"color":color, "index":i})
            time.sleep(DT)

        for i in range(self.NLEDS):
            self.setOff({"index":i})
            time.sleep(DT)


    def clearTarget(self, kwargs):
        self.ALL_STOP = False
        self.all_off()

    def is_pissed(self, test):
        """
        Returns true if any values in self.history are less than the test
        value.
        """
        rs = [1 for val in self.history if val<test]

        print test
        print self.history
        if rs: 
            print "PISSED"
        else:
            print "NOT PISSED"
        return rs or False


    def sensor_callback(self, sensor_values):
        STAGE1 = 15
        STAGE2 = 30
        self.led.all_off()
                
        val1 = sensor_values[0][1]
        val2 = sensor_values[2][1]


        if val2 < 200:
            self.led.fillRGB(155,155, 0, 0, self.NLEDS)
            self.led.update()


        self.history.append(val1);
        self.history.pop(0)

        index = self.NLEDS - val1
        
        percent = int(floor(100*float(index)/self.NLEDS))

        
        
        if index >= 0 and index < STAGE1 and sum(self.history) < len(self.history) * STAGE1:
            # Stage 1
            if not self.is_pissed(STAGE1):
                self.led.fillRGB(0, 255, 0, 0, index)
        elif index >=STAGE1 and index < STAGE2:
            # Stage 2
            if not self.is_pissed(STAGE2):
                self.led.fillRGB(0, 0, 255, 0, index)
        else:
            # Pissed
            self.led.fillRGB(255, 0, 0, 0, index)
        self.led.update()
