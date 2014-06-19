This is the ardyh.io websocket server. It acts as a message passing service and as an API to the ardyh AI. 


Currently I have a demo site setup at ardyh.solalla.com:9093. Check it out. The jjbot client app automatically points to 
ardyh.solalla.com.

The purpose of this server is to pass messages between devices and robots over the Internet. To use it, 
install the lilybot client on your Raspberry Pi. By default it points to173.255.213.55:9093. The in a broswer or smart phone
go to 173.255.213.55:9093 and you can see if your device connected. 



Dependencies
============
redis - 

### Python Packages

```
sudo pip install tornado
sudo pip install redis
```


The server listens on port 9093 by default

Start the Server
================

1. Got to `lilybot/server`
2. Run `python main.js`


Stop Server
===========

1. Get the process PID `sudo fuser 9093/tcp`
2. Kill the process `sudo kill PID`



## Connecting a Bot to ardyh

### Initial handshake

Bot should send an initial handshake JSON object.

```
{message: 
  {"bot_name":"",
   "bot_roles":[], 
}

```

**bot_name** - a unique identfiyer for the bot

**bot_roles** - a list of roles in the set {"router", "bot", "controller"}. The router role is for non tinternet connected use. the controller role is for user interfaces usually  with a web or mobile app.
              
 
#### Commands

A typical command will have the following JSON structure.

```
  {"command":"",
   "kwargs":{},
   }

```

**command** -  a string with the command name. This uses is a RPC model 

**kwargs** - an object whose keyword/values are arguements to the command.


A bot needs to register there commands.









