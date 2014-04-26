#!/bin/bash
# This script runs the BrickPi_Python JJ Car example server.
# written by Wil Black wilblack21@gmail.com Oct. 25 2013

# Start bluetooth discovery
# hciconfig hci0 piscan

cd  /home/pi/projects/lilybot/web_client
#sudo chmod 755 RPi_Server_Code.py

NOW=$(date +"%Y-%m-%dT%T %Z")
echo "[$NOW] Starting lilybot server"

python -m SimpleHTTPServer 9010
