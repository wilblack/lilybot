#!/bin/bash
# This script runs the BrickPi_Python JJ Car example server.
# written by Wil Black wilblack21@gmail.com Oct. 25 2013

# Start bluetooth discovery
# hciconfig hci0 piscan

export PYTHONPATH=$PYTHONPATH:/home/pi/projects/RPi-LPD8806:/home/pi/projects/BrickPi_Python:/home/pi/projects/GrovePi

cd  /home/pi/projects/lilybot/rpi_client
#sudo chmod 755 RPi_Server_Code.py

NOW=$(date +"%Y-%m-%dT%T %Z")
echo "[$NOW] Starting and ardyh client"

modprobe i2c-bcm2708
modprobe i2c-dev

python main.py
