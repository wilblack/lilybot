#!/bin/bash

# This script isused to tstart the mjepeg-streamer srerver. 
# Written by Wil Black wilblack21@gmail.com. Nov. 24 2013

mkdir /tmp/stream

# Not sure what this does but it needs to be here. 
raspistill --nopreview -w 1280 -h 960 -q 10 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 &
#raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 &

# Start the server
LD_LIBRARY_PATH=/usr/local/lib /usr/local/bin/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/projects/lilybot/rpi_client/stream -p 8081"

