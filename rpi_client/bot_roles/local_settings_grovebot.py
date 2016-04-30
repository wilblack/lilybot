
    """
    Router.py uses bot_packages in this file to setup command and sensor value routing to the correct bot_role.
    """

    UPDATE_SENSOR_DT = 5
    SENSOR_PUBLISH_DT = 10
    LOG_DTFORMAT = "%Y-%m-%dT%H:%M:%SZ"

    BOT_ROLES = ["grovebot"]
    BOT_SUBSCRIPTIONS = ['ardyh/bots/rpi5']
    BOT_CHANNEL = "ardyh/bots/rpi1"

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