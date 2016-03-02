from grovepi.grove_i2c_digital_light_sensor.grove_i2c_digital_light_sensor import Tsl2561, I2C_SMBUS, I2C_ADDRESS

print "Hello"
TSL2561 = Tsl2561()
TSL2561._init__(I2C_SMBUS, I2C_ADDRESS)
gain=0

def read():
    
    val = TSL2561.readLux(gain)
    out = {
        "ambient": val[0],
        "IR": val[1],
        "_ambient": val[2],
        "_IR": val[3],
        "_LUX": val[4]
    }
    TSL2561._control(_POWER_DOWN)
    print out
    return out

if __name__== "__main__":
    print "Starting"
    read()