import time
from math import pi

import RPi.GPIO as io
io.setmode(io.BCM)
 
pir_pin = 18
door_pin = 23
 
io.setup(pir_pin, io.IN)         # activate input
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

wheel_circumference = 0.5 * 2 * pi   # wheel diameter in meters
count = 0
then = time.time()
flag = False
spd = 0.0
dt = 0.0
total_dist = 0.0
while True:
    if io.input(door_pin):
	if flag:
	    flag = False
    else:
	if not flag:
	    flag = True
	    count = count + 1
	    now = time.time()
	    dt = now - then
	    total_dist = total_dist + wheel_circumference
	    spd = wheel_circumference / dt   
	    print "count: %s speed: %.1fm/s  dist: %.1fm \r" %(count, spd, total_dist)
	    then = now
