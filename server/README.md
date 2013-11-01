This is the ardyh.io websocket server. Currently I have a demo site setup at 173.255.213.55:9093. Check it out. 

The purpose of this server is to pass messages between devices and robots over the Internet. To use it, 
install the lilybot client on your Raspberry Pi. By default it points to173.255.213.55:9093. The in a broswer or smart phone
go to 173.255.213.55:9093 and you can see if your device connected. 



Dependencies
============

tornado - `pip install tornado` 

Start the Server
================

1. Got to `lilybot/server`
2. Run `python main.js`

The server will listen on port 9093
