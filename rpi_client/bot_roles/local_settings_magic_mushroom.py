"""
Router.py uses bot_packages in this file to setup command and sensor value routing to the correct bot_role.
"""

settings= {
    "bot_name":"rp2.solalla.ardyh",
    "bot_roles":"bot",
    "bot_packages":["magic_mushroom"],
    "subscriptions":['rp1.solalla.ardyh', 'rp3.solalla.ardyh'],
    
}
NLEDS = 32
DEFAULT_STATE = "#xmas"
UPDATE_SENSOR_DT = 5
LOOP_CALLBACK_DT = 0.2