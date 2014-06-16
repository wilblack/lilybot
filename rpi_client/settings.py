#URI_BASE = "ws://173.255.213.55:9093/ws"
URI_BASE = "ws://162.243.146.219:9093/ws"
VERBOSE = True
SENSORS = []

try:
    from local_settings import *
except:
    pass

URI = "%s?%s" %(URI_BASE, settings['bot_name'])  # This is only used for the ardyh connection, not for skynet
