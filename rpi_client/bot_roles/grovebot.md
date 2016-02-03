# Grovebot Instructions

## Initial Setup



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
