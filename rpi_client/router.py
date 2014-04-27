import json, ast
from settings import *
from time import sleep


try:
    print "Loading RPi-LPD8806"
    from raspledstrip.ledstrip import *
except SystemExit:
    print "[WARNING] RPi-LPD8806 bootstrap module found but no LEDS connected. Starting client anyways"
    print sys.exc_info()[0]

except:
    print "[WARNING] RPi-LPD8806 bootstrap module not found"
    print sys.exc_info()[0]


class Router(object):


    def __init__(self, config):


        self.JJBOT = JJBOT
        self.CTENOPHORE = CTENOPHORE



    

    def receive_message(message):
        if VERBOSE: print "Received message: %s" %(message)

        # Try to JSON deconde it
        try:
            # Using literal_eval to ahndle the unicoded keyword porblem.
            message = ast.literal_eval(message.data)
        except: 
            # If that fails use the good old json.loads()
            message = json.loads(message.data)


        if not "command" in message.keys(): 
            print "command not found in message"
            return

        cmd = message['command']
        kwargs = message.get('kwargs', {})
        if VERBOSE: print "command: %s\n" %(cmd), kwargs

        if cmd in self.core_commands:
            self.receive_core(cmd, kwargs)

        elif self.JJBOT:
            self.receive_jjbot(cmd, kwargs)

        elif self.CTENOPHORE:
            self.receive_ctenophore(cmd, kwargs)


    def receive_core(cmd, message):
        if VERBOSE: print "this is a core command"
            if cmd == "shutdown":
                shutdown()

            elif cmd == "restart":
                restart()


    def receive_ctenophore(cmd, kwargs):
        
        if VERBOSE: print "this is a ctenophore message"
        

        if cmd == "setMode":
            if VERBOSE: print "called setMode()"

        elif cmd == "setRGB":
            
            r,g,b = self.hex2rgb(kwargs["color"])
            if VERBOSE: print "calling setRGB(%s,%s,%s,%s)" %(kwargs["index"], r, g, b)
            self.led.setRGB(kwargs["index"], r, g, b)
            self.led.update()


        elif cmd == "setOff":
            if VERBOSE: print "called setOff()"

        elif cmd == "fillRGB":
            r,g,b = self.hex2rgb(kwargs["color"])
            if VERBOSE: print "called fillRGB()"

        elif cmd == "fillOff":
            if VERBOSE: print "called fillOff()"

        elif cmd == "allOff":
            self.led.all_off()

        elif cmd == "target"
            self.led.all_off()
            width = 5 # Total length will be 2 8 width + 1
            index = kwargs["index"]

            for i in range(width,0, -1):
                lefti = index -i
                righti = index+i 

                if righti < NLED-1:
                    self.led.setRGB(righti, 255,  0, 0)
                if lefti > 0:
                    self.led.setRGB(lefti, 255,  0, 0)
                self.led.update()





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


    def receive_jjbot(cmd, kwargs):
        if message == 'u' :
                self.log("Running Forward")
                BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
            
            elif message == 'd' :
                self.log("Running Reverse")
                BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
            
            elif message == 'r' :
                self.log("Turning Right")
                BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = -200  #Set the speed of MotorA (-255 to 255)
            
            elif message == 'l' :
                self.log("Turning Left")
                BrickPi.MotorSpeed[PORT_A] = -200  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
            
            elif message == 'b' :
                self.log("New Stopped")
                BrickPi.MotorSpeed[PORT_A] = 0
                BrickPi.MotorSpeed[PORT_D] = 0

            # Wil's added capabilites
            elif message == "nl":
                self.log("Nudge Left")
                BrickPi.MotorSpeed[PORT_A] = 0  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
                time.sleep(.5)
                BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)
              
            elif message == "nr":
                self.log("Nudge Right")
                BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = 0  #Set the speed of MotorA (-255 to 255)
                time.sleep(.5)
                BrickPi.MotorSpeed[PORT_A] = 200  #Set the speed of MotorA (-255 to 255)
                BrickPi.MotorSpeed[PORT_D] = 200  #Set the speed of MotorA (-255 to 255)


            elif message == "ll":
                self.log("Look Left")
                BrickPi.MotorSpeed[PORT_C] = -1*self.LOOK_SPEED
                time.sleep(self.LOOK_DT)
                # BrickPi.MotorSpeed[PORT_C] = -1*self.LOOK_SPEED
                # time.sleep(self.LOOK_DT)
                BrickPi.MotorSpeed[PORT_C] = 0

            elif message == "lr":
                self.log("Look Right")
                BrickPi.MotorSpeed[PORT_C] = self.LOOK_SPEED
                time.sleep(self.LOOK_DT)
                # BrickPi.MotorSpeed[PORT_C] = self.LOOK_SPEED
                # time.sleep(self.LOOK_DT)
                BrickPi.MotorSpeed[PORT_C] = 0

            elif message == "start-camera-1":  # Shutdown
                self.log("Starting camera")
                try:
                    self.bot.startCamera()
                except Exception, e: 
                    print e

            elif message == "stop-camera-1":  # Stop camera
                self.log("Stopping Camera")
                self.bot.stopCamera()


            elif message == "x":  # Shutdown
                self.log("Shutting down")
                shutdown()
            elif message == "y":  # Shutdown
                restart()
            
            BrickPiUpdateValues()                # BrickPi updates the values for the motors



class Ctenophore(object):

    def __init__(self):
        pass


