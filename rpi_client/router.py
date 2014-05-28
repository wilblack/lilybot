"""
A Mdule to handle routing of commands and messages to the 
various bot_roles and defined in bot_roles/.

"""
import json, ast
from settings import CTENOPHORE, JJBOT, VERBOSE

from bot_roles.core import Core
from bot_roles.ctenophore import Ctenophore
from bot_roles.jjbot import JJBot


class Router(object):

    def __init__(self):

        self.JJBOT = JJBOT
        self.CTENOPHORE = CTENOPHORE
        self.core = Core()

        if self.CTENOPHORE:
            self.ctenophore = Ctenophore()

        if self.JJBOT:
            self.jjbot = JJBot()

    def received_message(self, message):
        if VERBOSE: print "[Router.received_message] Received message: %s" %(message)
        # Try to JSON deconde it
        
        try:
            # Using literal_eval to ahndle the unicoded keyword porblem.
            message = ast.literal_eval(message.data)
        except:
            # If that fails use the good old json.loads()
            print "[Router.recieved_message()] Could not load message.data"
            import pdb; pdb.setm_trace()
            message = json.loads(message.data)
            
            
        if not "command" in message.keys(): 
            if 'sensor_values' in message['message'].keys():
                getattr(self.ctenophore, 'sensor_callback')(message['message']['sensor_values'])
                return
            else:
                return

        cmd = message['command']
        kwargs = message.get('kwargs', {})

        # if VERBOSE: print "command: %s\n" %(cmd), kwargs

        if cmd in self.core.commands:
            getattr(self.core, cmd)(kwargs)

        elif self.JJBOT and cmd in self.jjbot.commands:
            getattr(self.jjbot, cmd)(kwargs)

        elif self.CTENOPHORE and cmd in self.ctenophore.commands:
            getattr(self.ctenophore, cmd)(kwargs)

        else:
            print "%s not recognized as a valid command" % (cmd)

        