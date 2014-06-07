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
    def __init__(self, name, ctenophore, output_queue, nleds):
        super(PassiveThread, self).__init__()
        
        self.name = name
        self.ctenophore = ctenophore
        self.output_queue  = output_queue
        self.stoprequest = threading.Event()
        self.nleds = nleds

    def run(self):
        print "Starting thread %s" %(self.name)
        while not self.stoprequest.isSet():
            #self.ctenophore.fillRGB({"color":"#22FF33"})
            color = ('#%06X' % randint(0,256**3-1))
            self.ctenophore.pulse({"color":color})

            reverse = randint(0,2)
            if reverse > 0:
                self.ctenophore.pulse({"color":color, "direction":"reverse"})
            
            PULSE_DT = randint(8, 12)
            time.sleep(PULSE_DT)              # sleep for 200 ms


    def join(self, timeout=None):
        self.stoprequest.set() # Turns off the thread if it already started
        super(WorkerThread, self).join(timeout)


class BlinkThread (PassiveThread):
    """
    A thread the blinks every so often
    """

    def run(self):
        print "Starting thread %s" %(self.name)
        while not self.stoprequest.isSet():
            #self.ctenophore.fillRGB({"color":"#22FF33"})
            color = ('#%06X' % randint(0,256**3-1))
            index = randint(0,self.nleds)

            self.ctenophore.setRGB({"color":color, "index":index})
            time.sleep(randint(1,3))
            self.ctenophore.setRGB({"color":"#000000", "index":index})

            DT = randint(2, 4)
            time.sleep(DT)              # sleep for 200 ms


class CommandThread(threading.Thread):
    """
    A thread to handle responses to commands and sensor_values.
    It runs the command once and shuts down.
    """

    def __init__(self, ctenophore, command, kwargs):
        super(CommandThread, self).__init__()
        self.ctenophore = ctenophore
        self.command = command
        self.kwargs = kwargs

    def run(self):
        print "\n\n[CommandThread.run(%s)]" %self.command
        getattr(self.ctenophore, self.command)(self.kwargs)
        
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
        output_queue = Queue.Queue()
        # Start passive thread
        self.passiveThread = PassiveThread("Passive Thread", self, output_queue, self.NLEDS)
        #self.passiveThread.setDaemon(True)
        self.passiveThread.start()

        output_queue2 = Queue.Queue()
        self.blinkThread = BlinkThread("Blink Thread", self, output_queue, self.NLEDS)
        self.blinkThread.start()
        
        output_queue3 = Queue.Queue()
        self.blinkThread2 = BlinkThread("Blink Thread 2", self, output_queue, self.NLEDS)
        self.blinkThread2.start()
        
        output_queue4 = Queue.Queue()
        self.blinkThread3 = BlinkThread("Blink Thread 2", self, output_queue, self.NLEDS)
        self.blinkThread3.start()


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
        """
        kwargs
        - index
        - width

        """
        # Should move this to a thread
        self.led.all_off()
        nrepeat = 4
        dt = 0.2
        
        width = int(kwargs.get('width', '5'))   # Total length will be 2 8 width + 1
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
        # Should move this to a thread
        DT = 0.005
        color = kwargs['color']
        direction = kwargs.get('direction', 'forward')

        if direction == 'forward':
            seq = range(self.NLEDS)
        elif direction == 'reverse':
            seq = range(self.NLEDS, 0, -1)

        for i in seq:
            self.setRGB({"color":color, "index":i})
            time.sleep(DT)

        for i in seq:
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


    def sensor_callback(self, sensor_package, sensor_values):
        
        STAGE1 = 15
        STAGE2 = 30
        #self.led.all_off()
        
        try:
            getattr(self, "%s_sensor_callback" %sensor_package)(sensor_values)
        except:
            pass


    def grovebot_sensor_callback(self, sensor_values):
        #import pdb; pdb.set_trace()
        if sensor_values['slider'] == 1:
            self.led.fillRGB(255, 0, 255, 0, self.NLEDS)
        
        if sensor_values['touch'] == 1:
            self.led.fillRGB(0, 255, 255, 0, self.NLEDS)

        if sensor_values['sound'] > 350:
            self.led.fillRGB(0, 0, 255, 0, self.NLEDS)

        if sensor_values['light'] <200:
            self.led.fillRGB(100, 100, 100, 0, self.NLEDS)
        if sensor_values['light'] >= 200:
            self.all_off()


    def jjbot_sensor_callback(self, sensor_values):
        
        val1 = sensor_values[0][1]
        val2 = sensor_values[2][1]


        if val2 < 200:
            self.led.fillRGB(155,155, 0, 0, self.NLEDS)
            self.led.update()

        self.history.append(val1)
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


class MagicMushroom(Ctenophore):
    """
    This class is used to control the lights for the magic mushroom project. 
    It must handle sensor_values from a grovebot and a jjbot. It differs from
    ctenophore in that its first STOCK_HEIGHT leds are used in the mushroom 
    'stock', the remaing are used in the mushroom 'cap'  
    """
    
    
    def __init__(self):

        self.commands = ['setRGB', 'fillRGB', 'target', 'allOff', 'color_cap' ]

        # Initialize Lights, this does not belong here.
        self.NLEDS = NLEDS
        self.STOCK_HEIGHT = 7
        self.ALL_STOP = False
        self.led = LEDStrip(self.NLEDS)
        self.led.all_off()

        self.cap_on = False
        self.target_on = False
        
        self.history = [255, 255, 255]
        if VERBOSE: print "Initializing %s LEDS" %(self.NLEDS)
        
        for i in range(0, self.NLEDS):
            self.led.setRGB(i, 0,255,255)
            self.led.setRGB(self.NLEDS - i, 255, 255, 0)
            self.led.update()
            sleep(0.01)
            self.led.all_off()


        


    def grovebot_sensor_callback(self, sensor_values):
        
        if sensor_values['slider'] == 1:
            # Turns of passive threads
            #self.led.fillRGB(200, 0, 255, self.STOCK_HEIGHT+1, self.NLEDS)
            print "%s" %self.cap_on    
            if not self.cap_on:
                self.cap_on = True
                self.color_cap({'color':"#FF0000"})
        else:
            if self.cap_on:
                self.allOff({})
                self.cap_on = False
            

        if sensor_values['touch'] == 1:
            # Make it tingle at a point
            print 'touch = 1'
            if not self.target_on:
                kwargs = {'index': self.STOCK_HEIGHT + 10,
                          'width': 8}
                ct = CommandThread(self, 'target', kwargs)
                print "\n\nStarting ct thread\n\n"
                ct.start()
                self.target_on = True
        else:
            if self.target_on:
                self.target_on = False

            #self.led.fillRGB(0, 255, 255, 0, self.NLEDS)

        if sensor_values['sound'] > 200:
            self.led.fillRGB(0, 0, 255, self.STOCK_HEIGHT+1, self.NLEDS)


        if sensor_values['light'] <200:
            self.led.fillRGB(100, 100, 100, self.STOCK_HEIGHT+1, self.NLEDS)
        
        # if sensor_values['light'] >= 200:
        #     self.all_off()

    def green_cap(self, kwargs=None):

        self.led.fillRGB(0, 255, 0, self.STOCK_HEIGHT+1, self.NLEDS)
        index = 1
        while index < (self.NLEDS - self.STOCK_HEIGHT):
            self.led.setRGB(self.STOCK_HEIGHT + index, 255, 255, 255)
            index += 4
        
        self.led.update()

    def color_cap(self, kwargs):
        """
        kwargs:
         - color: an hex color string i.e.  '#00DD00'
        """
        
        r,g,b = hex2rgb(kwargs['color'])
        self.led.fillRGB(r, g, b, self.STOCK_HEIGHT+1, self.NLEDS)
        index = 1
        
        while index < (self.NLEDS - self.STOCK_HEIGHT):
            self.led.setRGB(self.STOCK_HEIGHT + index, 255, 255, 255)
            index += 4
        
        self.led.update()
        
        