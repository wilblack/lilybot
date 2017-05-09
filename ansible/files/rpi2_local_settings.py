"""
Router.py uses bot_packages in this file to setup command and sensor value routing to the correct bot_role.
"""


# DEPRACTED Feb. 2, 2016
settings= {
    #"bot_name":"rpi1.solalla.ardyh",
    #"bot_roles":"bot",
    #"bot_packages":["grovebot"],
    #"subscriptions":[],
}
# The Ardyh Hub IP
HUB_IP = "192.168.0.106"


UPDATE_SENSOR_DT = 10
SENSOR_PUBLISH_DT = 20
LOG_DTFORMAT = "%Y-%m-%dT%H:%M:%SZ"

BOT_ROLES = ["grovebot"]
BOT_SUBSCRIPTIONS = ['ardyh/bots/rpi6']
BOT_CHANNEL = "ardyh/bots/rpi2"
BOT_PACKAGES = ["grovebot"]
BOT_NAME = "ardyh/bots/rpi2"


SENSORS =[

    # temp and humidty are confugured for a dht pro in port d4
    {'type':'temp',
     'default':0,
     },

    {'type':'humidity',
     'default':0,
     },

    # # Use this if you are using the analog light sensor
    # {'type':'light',
    #   'default':0,
    # },

    # Use this if you are using the TSL2561
    {'type':'lux',
     'default':0,
     },
    {'type':'channel0',
     'default':0,
     },
    {'type':'channel1',
     'default':0,
     },
    {'type':'gain_m',
     'default':0,
     },
    {'type':'timing_ms',
     'default':0,
     }

]