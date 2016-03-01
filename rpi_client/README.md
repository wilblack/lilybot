# THIS IS DERACATED SEE `rpi_clients/bot_roles/README.md`

## Install tornado web server
See http://www.remwebdevelopment.com/blog/python/simple-websocket-server-in-python-144.html for more info.


## Install LPD8806 Software.  
See https://github.com/adammhaile/RPi-LPD8806.git

```
git clone https://github.com/adammhaile/RPi-LPD8806.git
cd RPi-LPD8806
python setup.py install
```


## Install Autobahn Python (BETA)
We will be using Autbahn Python for our WebSocket client https://github.com/tavendo/AutobahnPython. We also follow the WAMP sub protocal using bith RPC's and Pub/Sub. 


```
sudo apt-get update
sudo apt-get sudo apt-get install python-dev
sudo pip install autobahn[twisted]
```

###Troubleshooting

First I got an error saying that zope.interface was not found so I did a `sudo pip install zope.interface` and got the following warning.

```
    ********************************************************************************
    WARNING:
    
            An optional code optimization (C extension) could not be compiled.
    
            Optimizations for this package will not be available!
    ()
    command 'gcc' failed with exit status 1
    ********************************************************************************
    Skipping installation of /usr/local/lib/python2.7/dist-packages/zope/__init__.py (namespace package)
    Installing /usr/local/lib/python2.7/dist-packages/zope.interface-4.1.1-nspkg.pth

```

It turned out that zope.interface could not be installed properly becuase I had not installed python-dev tools. So if you get this be sure and do a apt-get update and  then install pythone-dev tools.


## Grab the RPi-LPD8806 Repo by Adam Haile.

`git clone https://github.com/adammhaile/RPi-LPD8806`

## Raspberry Pi Command Line Shortcuts
To run these commands, you need the IP address of the Raspberry Pi and ssh into it. On Windows, you can use PuTTY or on
Mac/Linux you can use the console.

```
#to shutdown a Raspberry Pi
sudo shutdown -h now

#to reboot
sudo shutdown -r now
```

## Start the Server

### Start from Command Line



## Power

I bought a 6-AA 9V pack. I connected the wires and reversed the colors (red to black). This turnd on the red power light on the Pi but it did not boot. I ordered the same thing from Dexter and it worked, I guess I wasn't supposed to reverse the wires. I think I can hook these up in parallel and receive more juice. Look here http://batteryuniversity.com/learn/article/serial_and_parallel_battery_configurations



Then open the html Client by point a browser at the file. On the client site it will ask you to enter a hostname/ip address. This is the IP address of the Pi that you got from your router.
