#URI_BASE = "ws://173.255.213.55:9093/ws"
URI_BASE = "ws://162.243.146.219:9093/ws"
VERBOSE = True


# The sensor reading DT in seconds. 
UPDATE_SENSOR_DT = 1
LOOP_CALLBACK_DT = 2

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
SENSORS = []

try:
    from local_settings import *
except:
    print "Could not import local_settings"

URI = "%s?%s" %(URI_BASE, settings['bot_name'])  # This is only used for the ardyh connection, not for skynet
