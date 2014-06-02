#!/bin/sh

$INSTALL_GROVEPI=true

if $INTALL_GROVEPI; then

GROVEPI_DIR=/home/pi/projects/GrovePi

cd $GROVEPI_DIR/Script/

sudo chmod +x install.sh
sudo ./install.sh;

fi

