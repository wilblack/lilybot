# 1. Grovebot Instructions

## Initial Setup
You can use the seeed light sensor on port A2, or the digital light sensor on port I2C - 2.

### 1. Attach GrovePi and Sensors
Attac the BrovePi and sensors to the Pi. Then boot the Pi.
GrovePi uses Seeed sensors, below are the sensors I have currelty tested with Lilybot.

    | Curently supported sensors    |
    | Sensor                | Port  |
    |-----------------------|-------|
    | Temp and Humidity Pro | D4    |
    | Analog Light          | A2    |
    | Digital Light         | I2C-2 |
    | Sound                 | A1    |
    | Touch                 | D7    |
    | PIR                   | D3    |


### 2. Enable I2C
Run `sudo raspi-config` then in Advanced Setting enable I2C and load the I2C kernal module.


### 2. Install and Update the GrovePi Firmware.

**Install GrovePi.** After install the system will reboot.


    cd /home/pi/projects/
    git clone https://github.com/DexterInd/GrovePi.git
    cd GrovePi
    sudo chmod 755 install Scripts/install.sh
    Scripts/install.sh

**Update Firmware**


    cd /home/pi/projects/GrovePi/Firmware
    sudo chmod +x firmware_update.sh
    sudo ./firmware_update.sh




### 1. Configure the rpi_client with the bot package you are using

Copy a local setting file from `rpi_client/bot_roles/` into rpi_client/local_settings.py. Edit that file appropriately.

This is an example local_settings.py file. It is the bare minimum required. Besure and change the BOT_CHANNEL to
an appropriate unqiue channel name (this is used for MQTT messaging).

```#python

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

           # Use this if you are using the TSL2561
           {'type':'lux',
             'default':0,
           },

    ]

```


Then restart `lilybotd`

    sudo /etc/init.d/lilybotd restart

If the service won't start, you can troubleshoot with 
    
    cd rpi_clients
    sudo ./start_lilybot.sh



## Troubleshooting

*On Grovebot the PIR sensor does not work.*
If you are having trouble with the SMBus (for the light sensor on Grovebot for instance) you can user `i2cdetect` to debug.

```
# Query for the device. You may need to check 0 also. 
sudo i2cdetect 1
```

You should get something that looks like below, if you don't, try a different device number.


```
pi@rpi2 ~ $ sudo i2cdetect 1
WARNING! This program can confuse your I2C bus, cause data loss and worse!
I will probe file /dev/i2c-1.
I will probe address range 0x03-0x77.
Continue? [Y/n] Y
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- 04 -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --           
```

Then run the following

```
# Not sure what this does.
sudo modprobe i2c-bcm2708
sudo modprobe i2c-dev
lsmod

# Then reboot
sudo shutdown -r now
```


If you are installing a grovebot and get the following error then just reboot the Raspberry Pi manually `sudo shutdown -r now`.

```
All Done.
Check and reboot now to apply changes.
 
Restarting
3
2
1
shutdown: you must be root to do that!
```



### Links 
I2C documentation. The Raspberry Pi talks to the GrovePi using the SMBus and I2c.
http://www.lm-sensors.org/wiki/i2cToolsDocumentation



# 2. Magic Mushroom
An LED Strip web app that comes with serveral preset colors and light patterns. Demo URL
See demo here http://ctenophore.solalla.com/#/magic-mushroom 
