#!/bin/sh
sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install git-core -y
sudo apt-get install screen -y
sudo apt-get install ipython -y
sudo apt-get install python-pip -y
sudo apt-get install bluez -y
sudo apt-get install python-bluetooth -y

cd /home/pi
mkdir projects
cd projects 
git clone https://github.com/wilblack/lilybot.git

# Install this if using the Brick Pi
git clone https://github.com/DexterInd/BrickPi_Python.git

# Install this is using LED lights
git clone https://github.com/adammhaile/RPi-LPD8806

# Install GroverPi
git clone https://github.com/DexterInd/GrovePi

