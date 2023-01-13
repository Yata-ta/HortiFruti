#/******************************************************\#
         #Application Initialization Bash Script#                     
#\******************************************************/#


echo Initilization Bash Script!



# Dependencies Install and Upgrade
#####################################################

yes | sudo apt-get upgrade

yes | sudo apt-get install --upgrade python3.10

yes | sudo apt-get install --upgrade python3-pip

#sudo pip install --upgrade pip
yes | sudo pip install --upgrade setuptools

yes | sudo pip install --upgrade pigpiod


# Get Username by Input
#####################################################

echo Raspberry Username:
read USERNAME




# Git Pull
#####################################################

if [ -d "/home/$USERNAME/HortiFruiti" ]; then
    ### Take action if DIR exists ###

else
    ###  $DIR does NOT exists ### 
    mkdir /home/$USERNAME/HortiFruiti
fi


if [ ! -d /home/$USERNAME/HortiFruiti/.git ] then
    #sudo git clone git@github.com:Yata-ta/HortiFruti.git /home/jose/bashScript_test
    sudo git clone https://github.com/Yata-ta/HortiFruti /home/$USERNAME/HortiFruiti
    cd /home/$USERNAME/HortiFruiti
else
    cd /home/$USERNAME/HortiFruiti
    sudo git pull https://github.com/Yata-ta/HortiFruti

fi


# Stdlib Libraries
#####################################################
#sudo pip install os
#sudo pip install random
#sudo pip install datetime
#sudo pip install time
#sudo pip install colorama
#sudo pip install socket
#sudo pip install pickle
#sudo pip install sqlite3
#sudo pip install xml
#sudo pip install psycopg2
#sudo pip install multiprocessing


# External Libraries
#####################################################
sudo pip install --upgrade numpy
sudo pip install --upgrade pandas


# Run dependencies
#####################################################
sudo pigpiod


# Run main.py
#####################################################
cd /home/$USERNAME/HortiFruiti/src/
sudo python3 main.py DEBUG
#sudo python3 main.py NORMAL
