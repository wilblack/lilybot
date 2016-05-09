import time
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
print " mode ="+str(mode)
GPIO.cleanup()

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24

# Pins for Motor A (front left)
aBackward=16 # In 1
aForward=18 # In 2

# Pins for Motor B (front right)
bBackward=15 # In 3
bForward=13 # In 4



GPIO.setmode(GPIO.BOARD)
GPIO.setup(aForward, GPIO.OUT)
GPIO.setup(aBackward, GPIO.OUT)

GPIO.setup(bForward, GPIO.OUT)
GPIO.setup(bBackward, GPIO.OUT)

def forward(x):
    GPIO.output(aForward, GPIO.HIGH)
    GPIO.output(bForward, GPIO.HIGH)
    print "forwarding running  motor "
    time.sleep(x)
    GPIO.output(aForward, GPIO.LOW)
    GPIO.output(bForward, GPIO.LOW)

def reverse(x):
    GPIO.output(aBackward, GPIO.HIGH)
    GPIO.output(bBackward, GPIO.HIGH)
    print "backwarding running motor"
    time.sleep(x)
    GPIO.output(aBackward, GPIO.LOW)
    GPIO.output(bBackward, GPIO.LOW)

print "forward motor "
forward(3)
time.sleep(1)
print "reverse motor"
reverse(3)

print "Stopping motor"
GPIO.cleanup()
