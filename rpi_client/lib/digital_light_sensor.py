import sys 

sys.path.append("/home/pi/projects/GrovePi/Software/Python/grove_i2c_digital_light_sensor")
import grove_i2c_digital_light_sensor as dls

print "Hello"
TSL2561 = dls.Tsl2561()
TSL2561._init__(dls.I2C_SMBUS, dls.I2C_ADDRESS)
gain=0

def read():
    
    val = TSL2561.readLux(gain)
    out = {
        "ambient": val[0],
        "IR": val[1],
        "_ambient": val[2],
        "_IR": val[3],
        "lux": val[4]
    }
    TSL2561._control(dls._POWER_DOWN)
    print out
    return out

if __name__== "__main__":
    print "Starting"
    read()