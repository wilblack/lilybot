#!/bin/bash

# This script isused to tstart the mjepeg-streamer srerver. 
# Written by Wil Black wilblack21@gmail.com. Nov. 24 2013

mkdir /tmp/stream

# Start the server
LD_LIBRARY_PATH=/usr/local/lib /usr/local/bin/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/Projects/lilybot/rpi_client/camera_stream/www -p 8081"

