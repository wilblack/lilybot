## Install tornado web server
See http://www.remwebdevelopment.com/blog/python/simple-websocket-server-in-python-144.html for more info.

## Install Autobahn Python
We will be using Autbahn Python for our WebSocket client https://github.com/tavendo/AutobahnPython. We also follow the WAMP sub protocal using bith RPC's and Pub/Sub. 


```
pip install autobahn[twisted]
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



## Grab the RPi-LPD8806 Repo by Adam Haile.

`git clone https://github.com/adammhaile/RPi-LPD8806`


## Start the Server

### Start from Command Line

To manually start the server do the following.
Make sure BrickPi.py is on your python path.

```
export PYTHONPATH=$PYTHONPATH:/home/pi/Projects/BrickPi_Python
cd  ~/Projects/BrickPi_Python/Project Examples/Browser Controlled Robot
sudo chmod 755 RPi_Server_Code.py
python RPi_Server_Code.py
```

### Start on Boot

Copy `lilybotd` and `lilybot_camerad` to the `etc/init.d` and update the rc.d file.

```
sudo cp lilybotd /etc/init.d/.
sudo cp lilybotd_camera /etc/init.d/.

sudo update-rc.d lilybotd defaults
sudo update-rc.d lilybot_camerad defaults
```


Once the deamon starts it appears to tie up the port. You can see what ports are currently being used with

```
sudo netstat -lptu
sudo netstat -tulpn
```

You can find the processes that are listening on port 9093 with
```
sudo fuser 9093/tcp
```

### Power

I bought a 6-AA 9V pack. I connected the wires and reversed the colors (red to black). This turnd on the red power light on the Pi but it did not boot. I ordered the same thing from Dexter and it worked, I guess I wasn't supposed to reverse the wires. I think I can hook these up in parallel and receive more juice. Look here http://batteryuniversity.com/learn/article/serial_and_parallel_battery_configurations



Then open the html Client by point a browser at the file. On the client site it will ask you to enter a hostname/ip address. This is the IP address of the Pi that you got from your router.
