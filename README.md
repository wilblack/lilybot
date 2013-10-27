lilybot
=======

These are samples, demos, and libraries I use with the Mindsotrm EV3 and a Raspberry Pi with a BrickPi.

Materials
---------

* EV3 - $350
* Raspberry Pi - $40
* BrickPi - $45
* NXT Touch Sensors - $40
* NXT Ultra Sonic Sensor - $25
* SD Card - $12
* 6 AA with 9V out power suply - $3
* 9v Volt adaptors - $3


Set-Up the Raspberry Pi with BrickPi
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

Change your default log in shell from sh to bash. Run change shell `chsh` and when prompted enter `/bin/bash`. 
Then log out and log back in. 


Run the following code and grab some coffee, the second command takes awhile.

```
sudo apt-get update
sudo apt-get upgrade
```

Now install some librabries and helpful stuff

```
sudo apt-get install screen
sudo apt-get install ipython
sudo apt-get install python-pip

```

Now make a project directory and clone some github repos.

```
cd ~
mkdirProjects
cd Projects 
git clone https://github.com/DexterInd/BrickPi_Python.git
git clone https://github.com/wilblack/lilybot.git
```

Helpful Links
-------------

* Port Diagram http://www.dexterindustries.com/BrickPi/getting-started/attaching-lego/
* Articles on batteirs for the Rapsberry Pi
