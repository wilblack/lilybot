lilybot
=======

These are samples, demos, and libraries I use with Lego Mindsotrm EV3, Raspberry Pi and BrickPi. The goal of lilybot
is to provide an easy to use cloud based software deployment system for hobby/ametuer robotics. Currently lilybot
is focused on using a Raspberry Pi along with a BrickPi to communicate with Lego Mindsorm sensors and motors (EV3 Sensors 
are not currenlt supported by brick BrickPi, but EV3 motors do work fine). 


Materials
---------

Here is a list of materials I have used and how much they costs.


* EV3 - $350
* Raspberry Pi - $40
* BrickPi - $45
* NXT Touch Sensors - $40
* NXT Ultra Sonic Sensor - $25
* SD Card - $12
* 6 AA with 9V out power suply - $3
* 9v Volt adaptors - $3


1. Set-Up the Raspberry Pi with BrickPi
=======================================

I followed the instructions here http://www.dexterindustries.com/BrickPi/getting-started/pi-prep/ 
and downloaded the "wheezy" image and installed Win32DiskImager from http://sourceforge.net/projects/win32diskimager/. 
A zip file of the wheezy image is included in the` lib` folder and is named `2013.07.27_BrickPi_weezy_flavor`.


Config Wi-Fi
------------

Plug in an enternet cable and turn the raspberry on. ssh should be enabled by default. You can log in with 
`ssh pi@IP_ADDRESS` and use `raspberry` as the password. You will need to check your router to find out the Raspberry Pi's IP address.

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

Now install some librabries and helpful stuff. The first two are optional but I like to have them.

```
sudo apt-get install screen
sudo apt-get install ipython
sudo apt-get install python-pip

```

Now make a project directory and clone some github repos. This will place the gihub clones in `/home/pi/Projects/`.

```
cd ~
mkdir Projects
cd Projects 
git clone https://github.com/DexterInd/BrickPi_Python.git
git clone https://github.com/wilblack/lilybot.git

```

Install some Python pip packages

```
sudo pip install tornado
sudo pip install ws4py
```


2. Run jjbot
============

`jjbot` is based on the BrickPi's jj-car example and is found in `lilybot/jjbot`. T



Helpful Links
-------------

* Port Diagram http://www.dexterindustries.com/BrickPi/getting-started/attaching-lego/
* Articles on batteirs for the Rapsberry Pi
