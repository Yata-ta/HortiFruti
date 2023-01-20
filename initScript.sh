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
#read USERNAME




# Git Pull
#####################################################


if [ ! -d "/home/gabriel/shared/myfork/HortiFruti" ]; then
    ###  $DIR does NOT exists ### 
    #mkdir /home/$USERNAME/HortiFruiti
    mkdir /home/gabriel/shared/myfork/HortiFruti
    
fi

#/home/pedro/local/ZE/test
#/home/$USERNAME/HortiFruiti

if [ ! -d "/home/gabriel/shared/myfork/HortiFruti/.git" ]; then
    
    sudo git clone https://github.com/Yata-ta/HortiFruti.git /home/gabriel/shared/myfork/HortiFruti
    #sudo git clone git@github.com:Yata-ta/HortiFruti.git /home/jose/bashScript_test
    #sudo git clone https://github.com/Embedded-System-yatata/LOL.git /home/pedro/local/ZE/final2
    
    cd /home/gabriel/shared/myfork/HortiFruti
else
    #cd /home/pedro/local/ZE/test
    cd /home/gabriel/shared/myfork/HortiFruti
    #sudo git pull https://github.com/Yata-ta/HortiFruti.git
    #sudo git pull https://github.com/Embedded-System-yatata/LOL.git

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
sudo killall pigpiod
sudo pigpiod


# Run main.py
#####################################################
cd /home/gabriel/shared/myfork/HortiFruti/src
#sudo python3 main.py DEBUG
sudo python3 main.py NORMAL
