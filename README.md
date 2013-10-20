lilybot
=======

These are samples, demos, and libraries for the Mindsotrm EV3

Materials
=========

SD Card - $12

Set-Up the Raspbeery Pi with BrickPi
====================================

I followed the instructions here http://www.dexterindustries.com/BrickPi/getting-started/pi-prep/ 
and downloaded the "wheezy" image and installed Win32DiskImager from http://sourceforge.net/projects/win32diskimager/. 
A zip file of the wheezy image is included in the` lib` folder and is named `2013.07.27_BrickPi_weezy_flavor`.


Config Wi-Fi
------------

Plug in an enternet cable and turn the raspberry on. ssh should be enabled by default. You can log in with 
`ssh pi@IP_ADDRESS` and use `raspberry` as the password. You will net to check your router to find out the Pi's IP address.

You will need to configure your Pi for WiFi by editing the `/etc/network/interfaces` file. See here for more 
info http://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-occidentalis

After you edit the `interfaces` file, reboot the Pi and check for the Pi's IP address on your router, it may have changed. 
You should now be able to ssh in over Wi-Fi.


Install and Update Software
---------------------------

Run and grab a coffee. This second command takes awhile.

```
sudo apt-get update
sudo apt-get upgrade
```
Now install some helpful librabries

```
sudo apt-get install screen
sudo apt-get install ipython
```

