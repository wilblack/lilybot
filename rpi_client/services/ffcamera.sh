#!/bin/sh
ffserver -f /etc/ffserver.conf & 

raspivid -t 0 -w 320 -h 240 -fps 20 -vf -o - | ffmpeg -v verbose -r 5 -s 320x240 -f video4linux2 -i /dev/video0 http://localhost/webcam.ffm