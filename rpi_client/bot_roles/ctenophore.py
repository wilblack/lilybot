import sys, time
import threading, Queue

from datetime import datetime as dt
from random import randint
from time import sleep
from math import floor

from bot_roles.core import Core

from settings import *
from utils import hex2rgb, rgb2hex

try:
    print "Loading RPi-LPD8806"
    from raspledstrip.ledstrip import *
except SystemExit:
    print "[WARNING] RPi-LPD8806 bootstrap module found but no LEDS connected. Starting client anyways"
    print sys.exc_info()[0]

except:
    print "[WARNING] RPi-LPD8806 bootstrap module not found"
    print sys.exc_info()[0]

PULSE_DT = 30



class PassiveThread (threading.Thread):
    """

    """
    def __init__(self, name, ctenophore, output_queue, nleds):
        super(PassiveThread, self).__init__()

        self.name = name
        self.ctenophore = ctenophore
        self.output_queue = output_queue
        self.stoprequest = threading.Event()
        self.nleds = nleds

    def run(self):
        print "Starting thread %s" % (self.name)
        while not self.stoprequest.isSet():
            PULSE_DT = randint(8, 12)
            color = ('#%06X' % randint(0, 256**3-1))

            # reverse = randint(0, 2)
            # if reverse == 0:
            #     self.ctenophore.pulse({"color": color})
            # elif reverse == 1: 
            #     self.ctenophore.pulse({"color": color, "direction": "reverse"})
            self.ctenophore.pulse({"color": color})
            time.sleep(PULSE_DT)              # sleep for 200 ms

        if self.stoprequest.isSet():
            print "******** STOP IT ************"



    def join(self, timeout=None):
        self.stoprequest.set()  # Turns off the thread if it already started
        super(PassiveThread, self).join(timeout)


class BlinkThread (PassiveThread):
    """
    A thread the blinks every so often

    To stop the thread set thread.stoprequest.set()
    """

    def run(self):
        print "Starting thread %s" % (self.name)
        while not self.stoprequest.isSet():
            color = ("#%06X" % randint(0, 256**3-1))
            index = randint(0, self.nleds)

            self.ctenophore.setRGB({"color": color, "index": index})
            time.sleep(randint(3, 20))
            if not self.stoprequest.isSet():
                self.ctenophore.setRGB({"color": "#000000", "index": index})

        if self.stoprequest.isSet():
            print "******** STOP IT ************ %s" % self.name


class MotionThread (PassiveThread):
    """
    To stop the thread set thread.stoprequest.set()
    """

    def run(self):
        dt = 0.1
        print "Starting thread %s" % (self.name)
        offset = 0
        while not self.stoprequest.isSet():
            for i in range(0, self.ctenophore.NLEDS):
                val = (i + offset) % self.ctenophore.NLEDS
                if i % 3 == 0:
                    color = "#AA0000"
                elif i % 3 == 1:
                    color = "#00AA00"
                elif i % 3 == 2:
                    color = "#AAAAAA"
                r, g, b = hex2rgb(color)

                self.ctenophore.led.setRGB(val, r, g, b)
                offset = (offset + 1) % 3
            self.ctenophore.led.update()
            time.sleep(0.1)

        if self.stoprequest.isSet():
            print "******** STOP IT ************ %s" % self.name


class XmasFadeThread (PassiveThread):
    """
    A thread the blinks every so often

    To stop the thread set thread.stoprequest.set()
    """

    def run(self):
        colors = [[1,0,0], [0,1,0], [1,1,1]]
        colorIndex = 0;
        dt = 0.1
        print "Starting thread %s" % (self.name)
        while not self.stoprequest.isSet():
            for i in range(20, 256, 5):
                r, g, b = [c*i for c in colors[colorIndex]]
                self.ctenophore.led.fillRGB(r, g, b, 0, self.ctenophore.NLEDS)
                self.ctenophore.led.update()
                if self.stoprequest.isSet(): break
                time.sleep(dt)

            if self.stoprequest.isSet(): break

            for i in range(250, 19, -5):
                r, g, b = [c*i for c in colors[colorIndex]]
                self.ctenophore.led.fillRGB(r, g, b, 0, self.ctenophore.NLEDS)
                self.ctenophore.led.update()
                if self.stoprequest.isSet(): break
                time.sleep(dt)

            colorIndex = (colorIndex + 1) % (len(colors))

        if self.stoprequest.isSet():
            print "******** STOP IT ************ %s" % self.name


class CommandThread(threading.Thread):
    """
    A thread to handle responses to commands and sensor_values.
    It runs the command once and shuts down.

    Usage:
    myTrhead = CommandThread("Blink Thread 1", ctenphore, output_queue, nleds)

    Params:
        - ctenphore instance of eather Ctenophore or MagicMushroom
        - output_queue - Not really sure what this is used for
         nleds - The number of LEDS to use for lighting.


    kwargs['duration'] to set a duration in seconds to wait until calling
    kwargs['command2']

    """

    def __init__(self, ctenophore, command, kwargs):
        super(CommandThread, self).__init__()
        self.ctenophore = ctenophore
        self.command = command
        self.kwargs = kwargs

    def run(self):
        while not self.stoprequest.isSet():
            self.ctenophore.set_state({'state':'#off'})

            print "\n\n[CommandThread.run(%s)]" % self.command
            getattr(self.ctenophore, self.command)(self.kwargs)
            if 'duration' in self.kwargs.keys() and 'command2' in self.kwargs.keys():
                time.sleep(self.kwargs['duration'])
                print "runnning command2: %s" % self.kwargs['command2']
                getattr(self.ctenophore, self.kwargs['command2'])(self.kwargs['kwargs2'])


class TimerThread(threading.Thread):
    """
    A thread to handle responses to commands and sensor_values.
    It runs the command once and shuts down.

    kwargs['duration'] to set a duration in seconds to wait until calling
    kwargs['command2']

    """

    def __init__(self, ctenophore ):
        super(TimerThread, self).__init__()
        self.ctenophore = ctenophore

    def run(self):
        print "\n\n[TimerThread.run())]"

        while not self.stoprequest.isSet():
            inactive_dt = dt.now() - self.ctenophore.last_state_change
            if inactive_dt.seconds > 20:
                self.ctenophore.set_state({'state':'#random'})
            time.sleep(5)



class Ctenophore(Core):

    def __init__(self, socket):
        super(Ctenophore, self).__init__(socket)

        self.commands = ['setRGB', 'fillRGB', 'target', 'allOff' ]

        # Initialize Lights, this does not belong here.
        self.NLEDS = NLEDS
        self.ALL_STOP = False
        #self.PLENGTH = 15 # Number of LEDS to use on a pulse. If > NLEDS, NELDS is used.
        self.led = LEDStrip(self.NLEDS)
        self.led.all_off()
        self.history = [255, 255, 255]
        if VERBOSE: print "Initializing %s LEDS" %(self.NLEDS)

        self.start_sequence()

        # Create a single input and a single output queue for all threads.
        #output_queue = Queue.Queue()
        # Start passive thread
        #self.passiveThread = PassiveThread("Passive Thread", self, output_queue, self.NLEDS)
        #self.passiveThread.setDaemon(True)
        #self.passiveThread.start()

        #output_queue2 = Queue.Queue()
        #self.blinkThread = BlinkThread("Blink Thread", self, output_queue, self.NLEDS)
        #self.blinkThread.start()

        # output_queue3 = Queue.Queue()
        # self.blinkThread2 = BlinkThread("Blink Thread 2", self, output_queue, self.NLEDS)
        # self.blinkThread2.start()

        # output_queue4 = Queue.Queue()
        # self.blinkThread3 = BlinkThread("Blink Thread 2", self, output_queue, self.NLEDS)
        # self.blinkThread3.start()

    def start_sequence(self):
        if VERBOSE: print "Initializing %s LEDS" % (self.NLEDS)
        for i in range(self.NLEDS/2 - 12, self.NLEDS/2 + 12):
            self.led.setRGB(i, 0, 255, 255)
            self.led.setRGB(self.NLEDS - i, 255, 255, 0)
            self.led.update()
            sleep(0.01)
            self.led.all_off()

    def setRGB(self, kwargs):
        r, g, b = hex2rgb(kwargs["color"])
        self.led.setRGB(kwargs["index"], r, g, b)
        self.led.update()

    def setOff(self, kwargs):
        self.led.setOff(kwargs['index'])
        self.led.update()

    def fillRGB(self, kwargs):
        """
        kwargs
            - color - hex color code, i.g. '#4466FF'
            - start - zero-based starting index
            -end - zero-ending index
        """
        r, g, b = hex2rgb(kwargs["color"])
        start = kwargs.get("start", 0)
        end = kwargs.get("end", self.NLEDS)
        self.led.fillRGB(r, g, b, start, end)
        self.led.update()

    def allOff(self, kwargs={}):
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


    def sensor_callbackOLD(self, sensor_package, sensor_values):
        
        STAGE1 = 15
        STAGE2 = 30
        #self.led.all_off()

        try:
            getattr(self, "%s_sensor_callbackOLD" %sensor_package)(sensor_values)
        except:
            pass


    def grovebot_sensor_callbackOLD(self, sensor_values):
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


    def jjbot_sensor_callbackOLD(self, sensor_values):
        
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

    def __init__(self, socket):
        super(MagicMushroom, self).__init__(socket)

        self.commands = ['setRGB', 'fillRGB', 'target', 'allOff', 'color_cap', 'set_state' ]

        # Initialize Lights, this does not belong here.
        self.NLEDS = NLEDS
        self.STOCK_HEIGHT = 0
        self.PLENGTH = 15 # Number of LEDS to use on a pulse. If > NLEDS, NELDS is used.

        self.ALL_STOP = False
        self.led = LEDStrip(self.NLEDS)
        self.led.all_off()

        self.cap_on = False
        self.target_on = False
        self.sound_on = False
        self.last_state_change = dt.now()

        self.history = [255, 255, 255]

        self.dist_history = [0, 0, 0, 0, 0]  # Initial values
        self.dist_threshold = 100

        self.currentThread = None
        self.blinkThreads = []
        self.soundThread = None
        self.timerThread = []


        # Initially set stat to the random state.
        self.state = ''
        kwargs = {'state': DEFAULT_STATE}
        self.set_state(kwargs)

    def grovebot_sensor_callbackOLD(self, sensor_values):
        # Check the distance values
        self.dist_history.pop(0)
        self.dist_history.append(sensor_values['dist'])

        dist_count = len([ 1 for val in self.dist_history if val > self.dist_threshold])
        print "In grovebot_sensor_callbackOLD() with ", self.dist_history
        print dist_count

        if dist_count > 3: # We are above the threshld, so that meand nobody is near by
            # Turn off the lights
            self.set_state({'state':'#off'})
        else:
            # Turn on the lights becuase spmething is near by. 
            self.set_state({'state':'#FF0000'})


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
            if not self.sound_on:
                kwargs = {
                    'start': 0,
                    'end': self.NLEDS,
                    'color': '#FF5050',
                    'duration': 0.5,
                    'command2': 'allOff',
                    'kwargs2': {}
                }
                ct = CommandThread(self, 'fillRGB', kwargs)
                print "\n\nStarting ct thread\n\n"
                ct.start()
                self.soundThread = ct
                self.sound_on = True

        else:

            if self.sound_on:
                self.sound_on = False

        if sensor_values['light'] < 200:
            kwargs = {
                'color': '#2200AA',
                'start': 0,
                'end': self.STOCK_HEIGHT
            }
            print "Lights out: ", kwargs
            self.fillRGB(kwargs)
        # if sensor_values['light'] >= 200:
        #     self.all_off()

    def pulse(self, kwargs):
        # Should move this to a thread
        old_state = self.state
        self.set_state({'state':'#off'})
        color = kwargs['color']
        direction = kwargs.get('direction', 'forward')

        if self.PLENGTH > self.NLEDS: self.PLENGTH = self.NLEDS

        if direction == 'forward':
            seq = range(self.NLEDS + self.PLENGTH )
        elif direction == 'reverse':
            seq = range(self.NLEDS, 0, -1)

        
        for i in seq:
            #Turn on LED
            if i < self.NLEDS:
                self.setRGB({"color":color, "index":i})
            
            # Turn off LEDS
            j = (i-self.PLENGTH) % self.NLEDS
            print "turn on %s and turn off %s" % (i, j)
            self.setOff({"index":j})

        #self.set_state({'state':old_state})
        # for i in seq:
        #     self.setOff({"index":i})

    def set_state(self, kwargs):
        """
        Accepts a dict called kwargs

        Starts threads based on the kwargs['state']. 


        kwargs:
         - state [String] String, it must start with '#'. Possible states are
             '#off', 
             '#random', 
             '#red-white-blue', 
             '#green-purple'
             '#glow-warm',

             '#<HEXCOLOR>',

        """

        state = kwargs['state']
        print "[MagicMushroom.set_state()] with state", state

        print "[set_state] Turning everything off"
        self.allOff({})

        if self.currentThread:
            self.currentThread.stoprequest.set()

        for thread in self.blinkThreads:
            print "[set_state] setting stoprequest on %s" % thread
            thread.stoprequest.set()
        self.blinkThreads = []

        if state == '#off':
            return

        elif state == '#random':
            for i in range(0, 20):
                output_queue = Queue.Queue()
                thread = BlinkThread("Blink Thread %s" %i, self, output_queue, self.NLEDS)
                thread.start()
                self.blinkThreads.append(thread)

        elif state == '#red-white-blue':
            for i in range(0, self.NLEDS):
                if i % 3 == 0:
                    color = "#FF0000"
                elif i % 3 == 1:
                    color = "#FFFFFF"
                elif i % 3 == 2:
                    color = "#0000FF"
                r, g, b = hex2rgb(color)

                self.setRGB({"color": color, "index": i})
            self.led.update()

        elif state == '#xmas':
            for i in range(0, self.NLEDS):
                if i % 3 == 0:
                    color = "#AA0000"
                elif i % 3 == 1:
                    color = "#00AA00"
                elif i % 3 == 2:
                    color = "#AAAAAA"
                r, g, b = hex2rgb(color)

                self.setRGB({"color": color, "index": i})
            self.led.update()

        elif state == '#xmas-motion':
            output_queue = Queue.Queue()
            thread = MotionThread("Motion Thread", self, output_queue, self.NLEDS)
            thread.start()
            self.currentThread = thread

        elif state == '#xmas-fade':
            output_queue = Queue.Queue()
            thread = XmasFadeThread("Xmas Fade Thread", self, output_queue, self.NLEDS)
            thread.start()
            self.currentThread = thread

        elif state == '#green-purple':
            for i in range(0, self.NLEDS):
                if i % 2 == 0:
                    color = "#00FF00"
                elif i % 2 == 1:
                    color = "#FF00FF"
                r, g, b = hex2rgb(color)

                self.setRGB({"color": color, "index": i})

            self.led.update()

        elif state == '#glow-warm':

            self.led.fillRGB(r, g, b, self.STOCK_HEIGHT+1, self.NLEDS)
            self.led.update()

        else:
            # Assume is a hex-color
            print "Looking for color %s" % state
            r, g, b = hex2rgb(state)

            self.led.fillRGB(r, g, b, self.STOCK_HEIGHT+1, self.NLEDS)
            self.led.update()

        self.state = state
        self.last_state_change = dt.now()
