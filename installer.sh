#!/bin/sh

LILYBOT_PATH=/home/pi/projects/lilybot/

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install python-dev -y
sudo apt-get install git-core -y
sudo apt-get install screen -y
sudo apt-get install ipython -y
sudo apt-get install python-pip -y
sudo apt-get install bluez -y
sudo apt-get install python-bluetooth -y

echo "\n\n*****************************\n"
echo "Creating /home/projects/"
echo "\n*****************************\n"

cd /home/pi
mkdir projects
cd projects 

echo "\n\n*****************************\n"
echo "Cloning git repos /home/projects/"
echo "\n*****************************\n"

git clone https://github.com/wilblack/lilybot.git

# Install this if using the Brick Pi
git clone https://github.com/DexterInd/BrickPi_Python.git

# Install this is using LED lights
git clone https://github.com/adammhaile/RPi-LPD8806

# Install GroverPi
git clone https://github.com/DexterInd/GrovePi

echo "\n\n*****************************\n"
echo "Installing lilybot pip requirements"
echo "\n*****************************\n"

cd $LILYBOT_PATH
sudo pip install -r requirements.txt

echo "\n\n*****************************\n"
echo "Setting ardyh_client to start on boot."
echo "\n*****************************\n"

sudo cp rpi_client/ardyh_clientd /etc/init.d/.
sudo update-rc.d ardyh_clientd defaults
