#!/bin/bash

function get_bot_info
{
    echo "Enter a bot name (rpi1): " 
    read botName

    if [ -z $botName ] ; then
        botName="rpi1"
    fi


    selection=
    until [ "$selection" = "0" ]; do
        echo ""
        echo "Choose a bot package"
        echo "1 - none"
        echo "2 - jjbot"
        echo "3 - ctenophore"
        echo "4 - grovebot"
        echo "5 - magic_mushroom"
        echo ""
        echo -n "Enter selection: "
        read selection
        case $selection in
            1 ) botPackage="" ; selection=0 ; ;;
            2 ) botPackage="jjbot" ; selection=0 ; ;;
            3 ) botPackage="ctenophore" ; selection=0 ; ;;
            4 ) botPackage="grovebot" ; selection=0 ; ;;
            5 ) botPackage="magic_mushroom" ; selection=0 ; ;;
            * ) echo "Please enter a value between 1 and 5"
        esac
    done
}

get_bot_info

echo "Your bot name is \"$botName\""
echo "Your bot package is \"$botPackage\""
echo "Is this correct? [y/n]"
read isCorrect

if [ $isCorrect = "n" ] ; then
    get_bot_info
fi

echo "**********************************************"
echo " STARTING INSTALLATION. THIS MAY TAKE A WHILE "
echo "**********************************************"


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
sudo apt-get install python-smbus -y

echo "\n\n*****************************\n"
echo "Creating ~/projects/ and ~/.ssh/"
echo "\n*****************************\n"

mkdir ~/,ssh
cd /home/pi
mkdir projects
cd projects



echo "\n\n*****************************\n"
echo "Installing lilybot pip requirements"
echo "\n*****************************\n"

cd $LILYBOT_PATH
sudo pip install -r requirements.txt


echo "\n\n*****************************\n"
echo "Cloning git repos /home/projects/"
echo "\n*****************************\n"

git clone https://github.com/wilblack/lilybot.git

echo "\n\n*****************************\n"
echo "Setting ardyh_client to start on boot."
echo "\n*****************************\n"

sudo cp rpi_client/lilybotd /etc/init.d/.
sudo update-rc.d lilybotd defaults


echo "Copying interfaces file for Wi-Fi\n"
echo "The will look for a newtowrk named ardyhnet with passkey ardyhnet.\n"
echo "To change this edit /etc/network/interfaces"
sudo cp interfaces.lilybot /etc/network/interfaces



if [ $botPackge = "jjbot" ] ; then
    echo "Cloning BrickPi_Python repo"
    git clone https://github.com/DexterInd/BrickPi_Python.git
fi

if [ "$botPackage" == "ctenophore" ] || [ "$botPackage" == "magic_mushroom" ] ; then
    echo "Cloning RPi-LPD8806 for LED lights"
    git clone https://github.com/adammhaile/RPi-LPD8806
fi 

if [ $botPackage == "grovebot" ] ; then 
    echo "Cloning GroverPi"
    echo "You are about to launch the GrovePi installer from Dexter Industries."
    echo "You will need to start the SMBus after this reboots. See the lilybot"
    echo "README.md for instructions https://github.com/wilblack/lilybot"
    echo "It boils down to running i2c-bcm2708 and i2c-dev then checking the device"
    echo "with i2cdetect 1."
    echo ""
    echo "Press any key to continue."
    read tmp

    git clone https://github.com/DexterInd/GrovePi

    chmod 755 GrovePi/Script/install.sh
    GrovePi/Script/install.sh
fi





