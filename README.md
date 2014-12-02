

#lilybot

The goal of lilybot is to provide an easy to use cloud based software system for hobby/ametuer robotics, primarily focused on the Raspberry Pi. This repo contains samples, demos, and libraries to do things like reading sensor data, control motors, and handling realt-time networking with other lilybots over the Internet.  

The software components of lilybot consist of three main functions.

1. The Raspberry Pi client
  This application runs on the Raspberry Pi and automatically connects to the web server ardyh. Over this connection it can stream data and listen and responds to commands from other lilybots. Use `rpi_client/settings.py` what hardware is attached to the Raspberry and set other settings. Once running you can view the webpage at RASPBERRY_PI_IPADDRESS:9093.

2. The ~ardyh~ real-time socket web server
  This server attacks as a pub/sub server for lilybot clients. The rpi_client will automatically try to establish a web socket connection to a server running this application at `ws://173.255.213.55:9093/ws`. You can use this server or run your own instance.
  See a demo here http://ardyh.solalla.com


3. Web application clients. 


## 1. Hardware Packages

To configure a hardware package you need to edit `rpi_client/local_settings.py`


### JJbot
A Libaray to control Lego Mindsorm sensors and motors (EV3 Sensors 
are not currenlt supported by brick BrickPi, but EV3 motors do work fine) connected to a BrickPi.  

### Ctenophore
An LED Strip controller. This exposes a web api to control these https://www.adafruit.com/products/306

### GroveBot
bot_package: groverbot
A lilbary to interface with the GrovePi and its sensors.

#### Hardware
* 1 GrovePi 
* 1 Grove Temperature and Humidity Pro plugged into port D4 on the GrovePi.
* 1 Grove Light Sensor plugged into port A2 on the GrovePi.

### Magic Mushroom
An LED Strip web app that comes with serveral preset colors and light patterns. Demo URL
See demo here http://ctenophore.solalla.com/#/magic-mushroom 

# Getting Started

## 1. Install the Raspbian Operating System
If you already have a Raspberry Pi up and running you can skip to step 2. It is best to start with a freshly installed version of Rasbian.

Set up a new Raspberry Pi model B with the Raspbian distribution. I followed the instructions here http://www.raspberrypi.org/help/noobs-setup/. The guide has you install NOOBS. NOOBS is a startup program that let's you install different OS's on the Raspberry Pi. In this repo I use the Raspbian version unless otherwise noted (JJBOT uses a different version).  You will need an 8GB or bigger SD card to install Raspbian. 

Once you have NOOBS installed on the SD Card, connect the wi-fi dongle, enthernet cable, (monitor and keyboard if you have one) and finally boot up by connecting the power.

On first boot select the Raspbian operating system and click "i". This will takes a while. On successfult install the Rpi will reboot and you will find yourself at the rasp-conf screen. 

### Related Links

* NOOBS Download (Use NOOBS Lite if you have a ethernet network connection to the pi) `http://www.raspberrypi.org/downloads/`

* SD Formatter 4.0 - https://www.sdcard.org/downloads/formatter_4/

<div id="step2"></div>


----
## 2. Raspberry Pi Configuration with rasp-config
At this point you should have a fresh version of Rasbian installed and you should either be directly connected to the raspberry Pi or have access over SSH on an ethernet cable. We will configure Wi-Fi in the next step. 

* Open the raspi-config menu. From the terminal type `rasp-config` on the command line. 

* Change option 3 to boot to console. Choose option 3 and select "Console Text console, requiring login (default)"

* Under *Advanced Options* change the hostname to something more descriptive and unique. This is more import when running multiple RPi's. I use rpi1, rpi2, etc...

* Under *Advanced Options* enable the SPI kernal. This is used for ????

* Enable Camera

If you are not from the UK you may want to change the country code of the Raspberry Pi at this time. If so select *Finish* but **do not reboot** then follow the instruction below. If you do not want to change the country code, simply Finish and reboot.

* **(Optional) Keyboard Country Code** - By default the Raspberry py will be set with a keyboard country code of "gb" for Great Britian. You should change this to your country code. For me in the US of A its "us".

  To change this edit the `/etc/default/keyboard` file. Change the line to the appropriate country code.
    ```
    XKBLAYOUT=”us”

    ```


**Troubleshooting**

You may get the follwoing error when connecting to the Raspberry Pi over WiFi if you have already connected over ethernet. 

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
86:f8:37:41:9e:37:12:4f:f6:4b:65:be:9e:d6:27:b4.
Please contact your system administrator.
Add correct host key in /Users/wilblack/.ssh/known_hosts to get rid of this message.
Offending RSA key in /Users/wilblack/.ssh/known_hosts:4
RSA host key for 192.168.1.113 has changed and you have requested strict checking.
Host key verification failed.

```

To fix this, on the machine you are ssh'ing from (i.e. not the rPi) edit the `~/.ssh/known_hosts` and remove the line whihc points at you Raspberry Pi's IP address.


----
## 3. Install and Update Software

Download and run the installer script. Grab some coffee this takes awhile. This will make a directory `/home/pi/projects/` and put the github repos in there. 

```
source <(curl -s https://raw.githubusercontent.com/wilblack/lilybot/master/installer.sh)
```


## 4. Configure the rpi_client with the bot package you are using

* Copy a local setting file from `rpi_client/bot_roles/` into rpi_client/local_settings.py. Edit that file appropriately.

TODO Show Example.

This is an example local_settings.py file. It is the bare minimum required.

```
settings= {
    "bot_name":"rp4.solalla.ardyh",
    "bot_roles":"bot",
    "bot_packages":[],
    "subscriptions":[],

}
```

## 5. (Optional) Set the Raspberry Pi to reconnect if it looses connection to ardyh
Add the following line to `/etc/crontab`

```
*    * * *   root    /home/pi/projects/lilybot/rpi_client/restart.sh > /home/pi/restart.log
```

### Troubleshooting

If you are having trouble with the SMBus you can user `sudo i2cdetect 0` to debug.

```
# Query for the device. You may need to check 0 also. 
sudo i2cdetect 1

# Not sure what this does.
sudo modprobe i2c-bcm2708

sudo modprobe i2c-dev
lsmod
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

## 4. Attach hardware and reboot.

After all that is done we are finally ready to attach the bot package specific hardware and a Wi-Fi dongle. Omce you attach the appropraite hardware and Wi-Fi dongle reboot the Raspberry Pi (`sudo shutdown -r now`). Once rebotted the Raspberry Pi will look for a Wi-Fi network named *ardyhnet* with passkey *ardyhnet*. To change this you can edit `/etc/network/interfaces`.


----
## 6. Install Camera and Camera Software (Optional)


Here is a video showinghow to connect the camera to the Raspberry Pi http://youtu.be/GImeVqHQzsE 

Follow the instruction here http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi to install the software on the RPi. They are summarized below

**NOTE** First make sure the camera is enabled. Run `sudo raspi-config` and enable the camera.

#### Streaming with mjpg-streamer

1. Install software packages. 
	```sh
	cd ~/
	sudo apt-get install libjpeg8-dev imagemagick libv4l-dev
	sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h
	
	```
2. Then make a temp directory to download the MJPEG-Streamer zip file

	```sh
	mkdir ~/temp
	cd ~/temp
	wget http://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-182.zip
	unzip mjpg-streamer-code-182.zip
	cd mjpg-streamer-code-182/mjpg-streamer
	make mjpg_streamer input_file.so output_http.so
	
	sudo cp mjpg_streamer /usr/local/bin
	sudo cp output_http.so input_file.so /usr/local/lib/

	cp -R www ~/projects/lilybot/rpi_client/camera_stream/  # This is what I did but I don't think its right.
	
	```

3. Now we should be able to  start the camera. The code below will start 
the camera and a webserver on port 8080 that will stream the video. 
To see run the code and open a browser and point it at `http://RASPBERRYPI_IP:8080`

	```sh
	mkdir /tmp/stream
	raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0
	
	LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/jjbot/www"
	
	```
#### Websockets streaming with ffmpeg


1. Build and configure [ffmpeg](http://ffmpeg.org/) on the Rapsberry Pi. It takes a while. I followed the instructions [here](http://sirlagz.net/2012/08/04/how-to-stream-a-webcam-from-the-raspberry-pi/). It takes a while. Below are the steps from that link.

  1. Add the following lines into /etc/apt/sources.list
    
    ```
    deb-src http://www.deb-multimedia.org sid main
    deb http://www.deb-multimedia.org wheezy main non-free
    ```
  
  2. Run `apt-get update`
  3. Run `apt-get install deb-multimedia-keyring`
  4. Remove the second line from `/etc/apt/sources.list`
    
    ```
    deb http://www.deb-multimedia.org wheezy main non-free
    ```
  
  5. Make and directory for your project and cd into it then run `apt-get source ffmpeg-dmo`
  6. You should now have a folder called ffmpeg-dmo-0.11 <-- The version will change as time goes by.
  7. Change the directory to the folder containing the source. e.g. cd ffmpeg-dmo-0.11
  8. Run `./configure` to setup the source.
  9. Run `make && make install` to compile and install ffmpeg
if you are not running as root like I am, then you will need to run the above command with sudo

 
     
2. On the socket server install the stream-server.js script from https://github.com/phoboslab/jsmpeg
	
    ```
    npm install ws
    node stream-server.js yourpassword
    ```
3. Install ffmpeg on Raspberry Pi. Point it at ardyh.
	```
	ffmpeg -s 640x480 -f video4linux2 -i /dev/video0 -f mpeg1video -b 800k -r 30 http://example.com:8082/yourpassword/640/480/
	```

4. To view the stream, get the `stream-example.html` and `jsmpg.js` from the [jsmpeg](https://github.com/phoboslab/jsmpeg) project. Change the WebSocket URL in the `stream-example.html` to the one of your server and open it in your favorite browser.

##### Troubleshooting

I got the below error. It looks like it is just some man page stuff. 
```
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffprobe.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffserver.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-all.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffprobe-all.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffserver-all.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-utils.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-scaler.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-resampler.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-codecs.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-bitstream-filters.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-formats.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-protocols.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-devices.1': Permission denied
install: cannot create regular file `/usr/local/share/man/man1/ffmpeg-filters.1': Permission denied
make: *** [install-man] Error 1

```

Then I got this error `Cannot open video device /dev/video0: No such file or directory`. Checking config.log It looks like there were build errors. Almost like it was not configured from the Raspberry pi. So after searching the internet I found a [part 3](http://sirlagz.net/2013/01/07/how-to-stream-a-webcam-from-the-raspberry-pi-part-3/) to the orignal tutorial. In it it said there maybe some errors to the original source so use the github repo instead.

```
git clone git://source.ffmpeg.org/ffmpeg.git
cd ffmpeg
./configure
make && make install

```

*ffmpeg*
You can install `v4l2-ctl` to help troubleshoot with 
```
apt-get install v4l-utils v4l-conf
```

Could not get anything on /dev/video0/ even after running modprobe so I tried installing uv4l and uv4l-raspicam as per here http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14. But got the following error:

```
Setting up uv4l (1.9.5-1) ...
libkmod: ERROR ../libkmod/libkmod.c:554 kmod_search_moddep: could not open moddep file '/lib/modules/3.6.11+/modules.dep.bin'
dpkg: error processing uv4l (--configure):
 subprocess installed post-installation script returned error exit status 1
Setting up raspberrypi-bootloader (1.20140908-1) ...
Memory split is now set in /boot/config.txt.
You may want to use raspi-config to set it
.
.
.
.
dpkg: dependency problems prevent configuration of uv4l-raspicam:
 uv4l-raspicam depends on uv4l (>= 1.9.5); however:
  Package uv4l is not configured yet.
```

If you try to start the camera service with `start_server_camera.sh` and get the following error.

```sh
mkdir: cannot create directory `/tmp/stream': File exists
MJPG Streamer Version: svn rev: 
 i: folder to watch...: /tmp/stream/
 i: forced delay......: 0
 i: delete file.......: no, do not delete
 i: filename must be..: pic.jpg
 o: www-folder-path...: /home/pi/projects/lilybot/rpi_client/camera_stream/www/
 o: HTTP TCP port.....: 8081
 o: username:password.: disabled
 o: commands..........: enabled
mmal: mmal_vc_component_enable: failed to enable component: ENOSPC
mmal: camera component couldn't be enabled
mmal: main: Failed to create camera component
mmal: Failed to run camera app. Please check for firmware updates
```
The command that is failing is the `raspistill`. 
To fix this reboot? There is a thread here http://raspberrypi.stackexchange.com/questions/13764/what-causes-enospc-error-when-using-the-raspberry-pi-camera-module



#### Links
Post on Raspberry Pi forums. 
http://www.raspberrypi.org/forums/viewtopic.php?f=43&t=74949

PiCamera
http://picamera.readthedocs.org/en/release-1.3/index.html

A tutorial showing how to stream video with web sockets.
http://phoboslab.org/log/2013/09/html5-live-video-streaming-via-websockets

FFmpeg
http://ffmpeg.org/

jsmpeg - A javscript stream decoder for websockets
https://github.com/phoboslab/jsmpeg

#### Troubleshooting

 
----
# For Developers

## The Ardyh Client 

### Starting and Stoppping.
The ardyh client is ran as a a service command with the name ardyh_clientd. It can be controlled using `/etc/init.d/ardyh_clientd`. By default the installer script will registers this service to start on boot. For debugging you may not want this. To turn it off use
```
# Turn off start on boot for ardyh_cleintd
sudo update-rc.d -f ardyh_clientd remove
```

To view the current running ardyh_clientd use 
```
ps aux | grep ardyh_clientd
```

To view all threads where <PID> is gotten from the above command.
```
ps -e -T | grep <PID>
```


The ardyh client will start two applications. The first application is a web server running on port 9010 to set local settings for the bot. It is available at <IP_ADDRESS>:9010. 

The second is a websocket client that is confugred to connect to the ardyh server at `ws://173.255.213.55:9093/ws`

### Manually start rpi_client
```
cd rpi_clinet
./start_ardyh_client.sh
```


### Set up client to start on boot (Depracted, the installer.sh script does this now)
First edit `rpi_client/ardyh_clientd` so that `DAEMON_PATH` points at the rpi_client/ directory.

```
DAEMON_PATH="/home/pi/projects/lilybot/rpi_client" 
```


Copy `lilybotd` and `lilybot_camerad` to the `etc/init.d` and update the rc.d file.


```
sudo cp rpi_client/ardyh_clientd /etc/init.d/.
sudo cp rpi_client/lilybotd_camera /etc/init.d/.

sudo update-rc.d ardyh_clientd defaults
sudo update-rc.d lilybot_camerad defaults
```


You may need to do a `chmod 775` to make these executable. You can then start and staop the deamon with `sudo /etc/init.d/ardyh_cleint start`


Once the deamon starts it ties up the port. You can see what ports are currently being used with

```
sudo netstat -lptu
sudo netstat -tulpn
```




# Appendix

## A1. How to SSH in to a Raspberry Pi
* With Ethernet Cable
Plug in an enternet cable and turn the raspberry on. ssh should be enabled by default. You can log in with `ssh pi@IP_ADDRESS` and use `raspberry` as the password. You will need to check your router to find out the Raspberry Pi's IP address.


  * With console cable
Follow this guide to set up the console cable
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable/overview



## Adding SSH Key to GitHub

See [Generating SSH Keys](https://help.github.com/articles/generating-ssh-keys/) for more info.

```
ssh-keygen -t rsa -C "your_email@example.com"

# Add the public key to GtiHub Settings-->Deploy keys

# test with
ssh -T git@github.com
```


## A2. Adding passwordless login with authorized_keys on Rapsberry Pi

See http://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md

Copy local key to the Raspberry Pi


From your regular computer run (you may need to create .ssh/authorized_keys in the Pi first)
```
cat ~/.ssh/id_rsa.pub | ssh <USERNAME>@<IP-ADDRESS> 'cat >> .ssh/authorized_keys'

```



----
## A3. Wi-Fi Dongles and Configuring Wi-Fi

I use these wi-fi dongles by Gymle based on the Realtek RTL8192 chipset.  
http://www.amazon.com/gp/product/B004HYHZJY/ref=oh_details_o00_s00_i00 becuase they support wi-fi direct (see this guide http://dishingtech.blogspot.com/2012/01/realtek-wi-fi-direct-programming-guide.html). I have not tested wi-fi direct yet but have plans to in the future. 

Check here for a list of compatible wi-fi dongles http://elinux.org/RPi_USB_Wi-Fi_Adapters

In the terminal see if your wi-fi dongle is detected with ifconfig.
```
sudo ifconfig
```



You will need to configure your Pi for WiFi by editing the `/etc/network/interfaces` file. See here for more 
info http://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-occidentalis

You can use the interfaces template in the root directory named `interfaces.lilbot` 

Plug in the wifi dongle


```
// Back up the file first
sudo cp /etc/network/interfaces /etc/network/interfaces.bkp

sudo cp interfaces.lilybot /etc/network/interfaces

sudo vi /etc/network/interfaces

// After editing the file restart
sudo shutdown -r now
```

Change the file to read, where you enter your own ssid and password. 

```
auto lo

iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
allow-hotplug wlan0

iface wlan0 inet dhcp
    wpa-ssid "YOUR_SSID"
    wpa-psk "YOUR_PASSKEY"
```


After you edit the `interfaces` file, restart the wlan0 adapter. 
```
sudo ifdown wlan0
sudo ifup wlan0
```

If succesful you can check the RPi's IP address on your router or do a ifconfig. The IP address will have changed. 
You should now be able to ssh in over Wi-Fi. Note you may need to reboot before you can access the Internet.



----
## Ansible

You can keep and inventory of your Raspberry Pi robots in the `hosts` file in the project root. 

Check the status of all the ardyh_cliend deamons. 
```
ansible -i hosts rpi_bots -u pi -m shell -a '/etc/init.d/ardyh_clientd status' 
```

Restart all Raspberry Pi's
```

ansible -i hosts rpi_bots -u pi -m shell -a 'shutdown -r now' --sudo
```

Shutdown a single bot
```
ansible -i hosts rp1 -u pi --sudo -m shell -a 'shutdown -h now' --sudo
```


Helpful Links
-------------

* Port Diagram http://www.dexterindustries.com/BrickPi/getting-started/attaching-lego/
* Articles on batteirs for the Rapsberry Pi
