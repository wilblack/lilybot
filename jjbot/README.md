## Install tornado web server
See http://www.remwebdevelopment.com/blog/python/simple-websocket-server-in-python-144.html for more info.

```
sudo pip install tornado
```

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
