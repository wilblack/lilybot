URI_BASE = "ws://173.255.213.55:9093/ws"

settings= {
    "bot_name":"rp2.solalla.ardyh",
    "bot_roles":"bot",
    "bot_packages":["ctenophore"],
    "subscriptions":['rp1.solalla.ardyh', 'rp3.solalla.ardyh'],
    
    # These ar enot being used yet.
    "network_name":"ardyhnet",
    "network_pwd":"ardyhnet",
    "default_network_name":"ardyhnet",
    "default_network_pwd":"ardyhnet"
}


VERBOSE = True

try:
    from local_settings import *
except:
    pass

URI = "%s?%s" %(URI_BASE, settings['bot_name'])  # This is only used for the ardyh connection, not for skynet
