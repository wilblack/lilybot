# Lilybot Hub

The hub runs a message passing server (MQtt), hosts the system control web app, stores all sensor data locally, and can sync up to the cloud.


## Web App

**http://192.168.0.105:9093/index.html**

This is the homeMonitor web app server from `hub/homeMonitor/`
For developement you should run this server on your local machine. 



## Set up


### Start Hub on Boot

Copy `/hub/ardyh_hubd` to `/etc/init.d`


    sudo cp hub/ardyh_hubd /etc/init.d/.
    sudo update-rc.d ardyh_hubd defaults


To remove this or disable this

    sudo update-rc.d -f ardyh_hubd remove


You may need to do a `chmod 775` to make these executable. You can then start and stop the deamon with 

`sudo /etc/init.d/ardyh_hub start`
`sudo /etc/init.d/ardyh_hub stop`


Once the deamon starts it ties up the port. You can see what ports are currently being used with

```
sudo netstat -lptu
sudo netstat -tulpn
```


To view the current running ardyh_hubd use 
```
ps aux | grep ardyh_hubd
```

To view all threads where <PID> is gotten from the above command.
```
ps -e -T | grep <PID>
```

## Mosquitto Stuff
RPI Clients will publish to the channel `ardyh/bots/BOT_NAME`

Examples of mosquitto_sub

    mosquitto_sub -t "ardyh/bots/rpi1"
    mosquitto_sub -t "ardyh/bots/+"
    mosquitto_sub -v -t \$SYS/#
