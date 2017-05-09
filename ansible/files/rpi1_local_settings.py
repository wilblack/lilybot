"""
Router.py uses bot_packages in this file to setup command and sensor value routing to the correct bot_role.
"""

# DEPRACTED Feb. 2, 2016
settings= {
    # "bot_name":"rpi1.solalla.ardyh",
    # "bot_roles":"bot",
    # "bot_packages":["grovebot"],
    # "subscriptions":[],
}

# The Ardyh Hub IP
HUB_IP = "192.168.0.106"


UPDATE_SENSOR_DT = 15
SENSOR_PUBLISH_DT = 10

LOG_DTFORMAT = "%Y-%m-%dT%H:%M:%SZ"

BOT_ROLES = ["grovebot"]
BOT_SUBSCRIPTIONS = ['ardyh/bots/rpi6']
BOT_CHANNEL = "ardyh/bots/rpi1"
BOT_PACKAGES = ["grovebot"]
BOT_NAME = "ardyh/bots/rpi1"


SENSORS =[

    # temp and humidty are confugured for a dht pro in port d4
    {'type':'temp',
     'default':0,
     },

    {'type':'humidity',
     'default':0,
     },

    {'type':'light',
     'default':0,
     }
]