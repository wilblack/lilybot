#lilybot

The goal of lilybot is to provide an easy to use cloud based software system for hobby/ametuer robotics, primarily focused on the Raspberry Pi. This repo contains samples, demos, and libraries to do things like reading sensor data, control motors, and handling realt-time networking with other lilybots over the Internet.  

The software components of lilybot consist of three main functions.

1. The Raspberry Pi client
  This application runs on the Raspberry Pi and automatically connects to the web server ardyh. Over this connection it can stream data and listen and responds to commands from other lilybots. Use `rpi_client/settings.py` what hardware is attached to the Raspberry and set other settings. Once running you can view the webpage at RASPBERRY_PI_IPADDRESS:9093.

2. The ~ardyh~ real-time socket web server
  This server attacks as a pub/sub server for lilybot clients. The rpi_client will automatically try to establish a web socket connection to a server running this application at `ws://173.255.213.55:9093/ws`. You can use this server or run your own instance.

3. Web application clients. 


## Hardware Packages

To configure a hardware package you need to edit `rpi_client/local_settings.py`


### JJbot
A Libaray to control Lego Mindsorm sensors and motors (EV3 Sensors 
are not currenlt supported by brick BrickPi, but EV3 motors do work fine) connected to a BrickPi.  

### Ctenophore
An LED Strip controller. This exposes a web api to control these https://www.adafruit.com/products/306

### GrovePi
A lilbary to interface with the GrovePi and its sensors.


# Getting Started

## 1. Install the Raspbian Operating System
If you already have a Raspberry Pi up and running you can skip to step 2.

We will set up a new Raspberry Pi model B with the Rasbian distribution. I followed the instructions here http://www.raspberrypi.org/help/noobs-setup/. The guide has you install NOOBS. NOOBS is a startup program that let's you install different OS's on the Raspberry Pi. In this repo I use the Raspbian version unless otherwise noted (JJBOT uses a different version).  You will need an 8GB or bigger SD card to install Raspbian. 

Once you have NOOBS installed on the SD Card, connect the wi-fi dongle, enthernet cable, (monitor and keyboard if you have one) and finally boot up by connecting the power.

On first boot select the Raspbian operating system and click "i". This will takes a while. On successfult install the Rpi will reboot and you will find yourself at the rasp-conf screen. 


### Links

* NOOBS Download (Use NOOBS Lite if you have a ethernet network connection to the pi) `http://www.raspberrypi.org/downloads/`

* SD Formatter 4.0 - https://www.sdcard.org/downloads/formatter_4/

<div id="step2"></div>

## 2. Initial rasp-config Configuration
To get to the rasp-config screen type `rasp-config` on the command line. 

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




Install and Update Software
---------------------------
* Change option 3 to boot to console.

* Change hostname to something ore descriptive and unique. This is more import when running multiple RPi's

* Load the SPI kernal

* Enable Camera

Finsh and reboot. Once you reboot we will change your keyboard country code to what's appropriate for you, for me its US. 
* Keyboard Country Code
  By default the Raspberry py will be set with a keyboard country code of "gb" for Great Britian. You should change this to your country code. For me in the US of A its "us".

  To change this edit the `/etc/default/keyboard` file. Change the line to the appropriate country code.
    ```
    XKBLAYOUT=”us”

    ```


## 3. Configure Wi-Fi

I use these wi-fi dongles by Gymle based on the Realtek RTL8192 chipset.  
http://www.amazon.com/gp/product/B004HYHZJY/ref=oh_details_o00_s00_i00 becuase they support wi-fi direct (see this guide http://dishingtech.blogspot.com/2012/01/realtek-wi-fi-direct-programming-guide.html). I have not tested wi-fi direct yet but have plans to in the future. 

Check here for a list of compatible wi-fi dongles http://elinux.org/RPi_USB_Wi-Fi_Adapters

In the terminal see if your wi-fi dongle is detected with ifconfig.
```
sudo ifconfig
```


  * With Ethernet Cable
Plug in an enternet cable and turn the raspberry on. ssh should be enabled by default. You can log in with 
`ssh pi@IP_ADDRESS` and use `raspberry` as the password. You will need to check your router to find out the Raspberry Pi's IP address.


  * With console cable
Follow this guide to set up the console cable
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable/overview




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


## 4. Install and Update Software

Change your default log in shell from sh to bash. Run change shell `chsh` and when prompted enter `/bin/bash`. 
Then log out and log back in. 



Run the following code and grab some coffee, the second command takes awhile. This will make a directory `/home/pi/projects/` and put the github repos in there. 

```
wget https://raw.githubusercontent.com/wilblack/lilybot/ctenophore/apt-get-installer.sh
chmod 755 apt-get-installer.sh
./installer.sh
```


### Install Camera and Camera Software (Optional)


Here is a video showinghow to connect the camera to the Raspberry Pi http://youtu.be/GImeVqHQzsE 

Follow the instruction here http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi 
to install the software on the RPi. They are summarized below

**NOTE** First make sure the camera is enabled. Run `sudo raspi-config` and enable the camera.

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

Now we should be able to  start the camera. The code below will start 
the camera and a webserver on port 8080 that will stream the video. 
To see run the code and open a browser and point it at `http://RASPBERRYPI_IP:8080`

```
mkdir /tmp/stream
raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0

LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/jjbot/www"

```

To stop streaming use

```

```

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



Helpful Links
-------------

* Port Diagram http://www.dexterindustries.com/BrickPi/getting-started/attaching-lego/
* Articles on batteirs for the Rapsberry Pi
