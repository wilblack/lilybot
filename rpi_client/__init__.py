class ArdyhClient(TornadoWebSocketClient):
    """
    Web Socket client to connect to ardyh on start up.
    
    Data is passed back and forth using a message object. 
    the message object is a JSON Object with the following keywords

    - message
    -- name
    -- from
    -- channel 
    -- message
    -- command
    -- ardyh_timestamp - May not be present

    """

    def __init__(self, protocols, uri='ws://173.255.213.55:9093/ws?'):
        rs = super(ArdyhClient, self).__init__(uri, protocols)
        

        self.ARDYH_URI = uri
        self.LOG_DTFORMAT = "%H:%M:%S"
        self.CTENOPHORE = CTENOPHORE
        

        self.channel = settings['bot_name']

        # set the name to MAC address if not found.
        self.bot_name = settings['bot_name']
        self.bot_roles = settings['bot_roles']

        self.core = Core()
        self.router = Router()


    def opened(self):
        print "Connection to ardh is open"
        message = {'bot_name':self.bot_name, 
                   'bot_roles':self.bot_roles,
                   'mac':get_mac_address(),
                   'handshake':True,
                   'subscriptions':settings['subscriptions']
                   }


        self.send(message)

        if ["jjbot", "grovebot"] and settings["bot_packages"]:
            print "Registering IO Loop callback"
            sensors = tornado.ioloop.PeriodicCallback(self.loopCallback, LOOP_CALLBACK_DT*1000)
            sensors.start()


    def received_message(self, message):
        self.router.received_message(message)


    def send(self, message):
        """
        Message should be of the form {MESSAGE_OBJ}
        

        - message
        -- bot_name
        -- from
        -- message
        -- command
        -- channel 
        -- ardyh_timestamp - May not be present

        """

        channel = settings['bot_name']
        message.update({
            "bot_name":self.bot_name,
            "channel":self.channel
        })
        message = json.dumps(message)
        if VERBOSE: print "[ArdyhClient.send] Send message:\n\n%s" %(message) 
        try:
            super(ArdyhClient, self).send(message)
        except:
            print "[ERROR] Message not send() failed."
            print sys.exc_info()[0]

    def closed(self, code, reason=None):
        print "Closed down", code, reason
        
        ioloop.IOLoop.instance().stop()


    def log(self, message):
        now = dt.now().strftime(self.LOG_DTFORMAT)
        message = "[%s] %s" %(now, message)
        print message
        self.send(message)


    def loopCallback(self):
        if "jjbot" in settings["bot_packages"]:
            sensor_values = self.get_sensors_values('jjbot') # This is where to sensor values get sent to ardyh
            out = {"message": {"sensor_values":sensor_values, "sensor_package":"jjbot"} }

        if "grovebot" in settings["bot_packages"]:
            sensor_values = self.get_sensors_values('grovebot') # This is where to sensor values get sent to ardyh
            out = {"message": {"sensor_values":sensor_values, "sensor_package":"grovebot"} }

        self.send(out)


    def get_sensors_values(self, bot_package):
        if bot_package == 'jjbot':
            out = [
                ['PORT_1', BrickPi.Sensor[PORT_1]],
                ['PORT_2', BrickPi.Sensor[PORT_2]],
                ['PORT_3', BrickPi.Sensor[PORT_3]],
                ['PORT_4', BrickPi.Sensor[PORT_4]],
              ]
        if bot_package == 'grovebot':
            out = grovePiSensorValues.toDict()
        return out
