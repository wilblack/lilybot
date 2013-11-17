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
* Raspberry Pi Camera Module - $30
* Camera Module mount kit - $5
* NXT Touch Sensors - $40
* NXT Ultra Sonic Sensor - $25
* SD Card - $12
* 6 AA with 9V out power suply - $3
* 9v Volt adaptors - $3
* 12 rechargable AA  NiMH batteries - $15
* Rayovac PS3 battery charger - $20



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
sudo apt-get install bluez
sudo apt-get install python-bluetooth


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
sudo pup install pyreadlines
```


2. Install Camera and Camera Software
=====================================

Here is a video showinghow to connect the camera to the Raspberry Pi http://youtu.be/GImeVqHQzsE 



Follow the instruction here http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi 
to install the software on the RPi. They are summarized below

**NOTE** First make sure the camera is enabled. Run `sudo rasp-config` and enable the camera.

```
cd ~/
sudo apt-get install libjpeg8-dev imagemagick libv4l-dev
sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h

```
Then make a temp directory to download the MJPEG-Streamer zip file

```
mkdir ~/temp
cd ~/temp
wget http://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-182.zip
unzip mjpg-streamer-code-182.zip
cd mjpg-streamer-code-182/mjpg-streamer
make mjpg_streamer input_file.so output_http.so

sudo cp mjpg_streamer /usr/local/bin
sudo cp output_http.so input_file.so /usr/local/lib/
# sudo cp -R www /usr/local/www # This is what the tutorial says, i didn't do it becuase /usr/local/www does not exist.
cp -R www ~/Projects/lilybot/jjbot/  # This is what I did but I don't think its right.

```

Now we should be able to  start the camera

```
mkdir /tmp/stream
raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0

LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/jjbot/www"

```




3. Run jjbot
============

`jjbot` is based on the BrickPi's jj-car example and is found in `lilybot/jjbot`.



Helpful Links
-------------

* Port Diagram http://www.dexterindustries.com/BrickPi/getting-started/attaching-lego/
* Articles on batteirs for the Rapsberry Pi
