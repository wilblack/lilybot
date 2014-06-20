"""
Router.py uses bot_packages in this file to setup command and sensor value routing to the correct bot_role.
"""

settings= {
    "bot_name":"rp3.solalla.ardyh",
    "bot_roles":"bot",
    "bot_packages":["grovebot"],
    "subscriptions":[],
}

SENSORS =[
    {'type':'temp',
        'default':0,
       },

       {'type':'humidity',
        'default':0,
       },

       {'type':'sound',
        'default':0,
       },

       {'type':'light',
        'default':0,
       },

       {'type':'slider',
        'default':0,
       },

       {'type':'touch',
        'default':0,
       },

       {'type':'pir',
        'default':0,
       },

       {'type':'dist',
        'default':0,
       },

       {'type':'acc_xyz',
        'default':[0,0,0],
       },
]