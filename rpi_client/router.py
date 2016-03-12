"""
A module to handle routing of commands and messages to the 
various bot_roles and defined in bot_roles/.

"""

import json, ast
from settings import VERBOSE, BOT_PACKAGES

from bot_roles.core import Core


class Router(object):

    def __init__(self, socket):
        print "Initializing Router"
        self.socket = socket
        self.ctenophore = False
        self.jjbot = False
        self.magic_mushroom = False
        self.grovebot = False
        bot_packages = BOT_PACKAGES

        self.core = Core(self.socket)
        if 'ctenophore' in bot_packages:
            from bot_roles.ctenophore import Ctenophore
            self.ctenophore = Ctenophore(socket)

        if 'jjbot' in bot_packages:
            from bot_roles.jjbot import JJBot
            self.jjbot = JJBot(socket)

        if 'magic_mushroom' in bot_packages:
            from bot_roles.ctenophore import MagicMushroom
            self.magic_mushroom = MagicMushroom(socket)

        if 'grovebot' in bot_packages:
            from bot_roles.grovebot import Grovebot
            self.grovebot = Grovebot(socket)

    def received_message(self, raw_message):
        """
        Messages should be a JSON object with the following keywords

        data : {
            timestamp : "",
            bot_name : "",
            message : {
                command
                kwargs
            }
        }
        

        """

        
        if VERBOSE: print "[Router.received_message] Received message: %s" % (raw_message)
        # Try to JSON deconde it
        parsed = False
        try:
            # Using literal_eval to ahndle the unicoded keyword porblem.
            message = ast.literal_eval(raw_message.data)
            parsed = True
        except:
            # If that fails use the good old json.loads()
            print "[Router.recieved_message()] Could not load raw_message.data with ast.literal_eval"
        
        if not parsed:
            try:
                message = json.loads(raw_message.data)
                parsed = True
            except:
                print "[Router.recieved_message()] Could not load message.data with json.loads"
                print "Ignoring message"
                
                print raw_message
                return

        
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

            if self.grovebot and cmd in self.grovebot.commands:
                getattr(self.grovebot, cmd)(kwargs)
                received = True

            if not received:
                print "%s not recognized as a valid command" % (cmd)
            return

        
        if 'sensor_values' in message.keys():
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
