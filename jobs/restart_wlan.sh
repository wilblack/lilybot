#!/bin/bash
#Script to check the network connection

#Check network connection
if /sbin/ifconfig wlan0 | grep -q "inet addr:" ; then
    #Connection is good; do nothing
    echo "$(date "+%D [%H:%M:%S]") Connection is up"
else
    echo "$(date "+%D [%H:%M:%S]") Network connection down. Attempting to reconnect..."
    sudo /sbin/ifup --force wlan0
fi