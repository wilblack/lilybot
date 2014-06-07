"""
A Mdule to handle routing of commands and messages to the 
various bot_roles and defined in bot_roles/.

"""
import json, ast
from settings import VERBOSE, settings

from bot_roles.core import Core
from bot_roles.ctenophore import Ctenophore, MagicMushroom
from bot_roles.jjbot import JJBot



class Router(object):

    def __init__(self):

        self.ctenophore = False
        self.jjbot = False
        self.magic_mushroom = False
        self.grovebot = False
        bot_packages = settings['bot_packages']
        

        self.core = Core()
        if 'ctenophore' in bot_packages:
            self.ctenophore = Ctenophore()

        if 'jjbot' in bot_packages:
            self.jjbot = JJBot()

        if 'magic_mushroom' in bot_packages:
            self.magic_mushroom = MagicMushroom()

        if 'grovebot' in bot_packages:
            from bot_roles.grovebot import Grovebot
            self.grovebot = Grovebot



    def received_message(self, message):
        if VERBOSE: print "[Router.received_message] Received message: %s" %(message)
        # Try to JSON deconde it
        
        try:
            # Using literal_eval to ahndle the unicoded keyword porblem.
            message = ast.literal_eval(message.data)
        except:
            # If that fails use the good old json.loads()
            print "[Router.recieved_message()] Could not load message.data"
            message = json.loads(message.data)
            
        if "command" in message.keys(): 

            cmd = message['command']
            kwargs = message.get('kwargs', {})

            # if VERBOSE: print "command: %s\n" %(cmd), kwargs
            received = False
            if cmd in self.core.commands:
                getattr(self.core, cmd)(kwargs)
                received = True

            if self.jjbot and cmd in self.jjbot.commands:
                getattr(self.jjbot, cmd)(kwargs)
                received = True

            if self.ctenophore and cmd in self.ctenophore.commands:
                getattr(self.ctenophore, cmd)(kwargs)
                received = True

            if self.magic_mushroom and cmd in self.magic_mushroom.commands:
                getattr(self.magic_mushroom, cmd)(kwargs)
                received = True

            if not received:
                print "%s not recognized as a valid command" %(cmd)
            return

        if 'sensor_values' in message['message'].keys():
            received = False
            if self.jjbot:
                getattr(self.jjbot, 'sensor_callback')(message['message']['sensor_package'], message['message']['sensor_values'])
                received = True

            if self.ctenophore:
                getattr(self.ctenophore, 'sensor_callback')(message['message']['sensor_package'], message['message']['sensor_values'])
                received = True

            if self.magic_mushroom:
                getattr(self.magic_mushroom, 'sensor_callback')(message['message']['sensor_package'], message['message']['sensor_values'])
                received = True
            
            if not received:
                print "Senor values ignored. No bot_packge found"

