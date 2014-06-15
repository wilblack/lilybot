"""
Router.py uses bot_packages in this file to setup command and sensor value routing to the correct bot_role.
"""

settings= {
    "bot_name":"rp3.solalla.ardyh",
    "bot_roles":"bot",
    "bot_packages":["grovebot"],
    "subscriptions":[],

    "sensors":[
        {'type':'temp',
         'units':'C',
         'verbose':'Temperature'
        }
        ]
    
}
