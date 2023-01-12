## *************************************** ##
        ## Classes Repository file ##
## *************************************** ##
## ** Created by Gabriel Pizzighini and Pedro blank ** ## 


import os
import random as r
import datetime as dt
import time
import colorama as cl
import socket
import pickle
import RPi.GPIO as GPIO

# Creates de client for comunication with the server !! Deprecated !!
class Client():
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 2022

        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
    
    def readMeasures(self):
        data = self.socket.recv(4096)
        data = data.decode('utf-8')
        return eval(data)

    def close(self):
        self.socket.close()

# Server class which will output information form the simulator !! Deprecated !!
class Server(): 
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 2022

        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.conn, self.address = self.socket.accept()

    def sendMeasures(self, temp, hum, co2, o2, press):
        data = [temp, hum, co2, o2, press]
        data = str(data)
        data = data.encode()
        self.conn.send(data)

    def close(self):
        self.conn.close()

# creates a sensor class for simulation purposes 
class Sensor:
    def __init__(self,id,room,name,min,max):
        self.id = id
        self.name = name
        self.room = room
        self.value = 0
        self.min = min
        self.max = max

    def get_name(self):
        return self.name

    def start_increase_value(self):
        aux = self.min
        self.value = aux + 0.8
        self.min = self.value
    
    def start_decrease_value(self):
        aux = self.max
        self.value = aux - 0.8
        self.max = self.value

    def increase_value(self):
        self.value = self.value + 0.8
        return self.value

    def decrease_value(self):
        self.value = self.value - 0.8
        return self.value
    
    def act_increase_value(self):
        self.value = self.value + 1
        return self.value

    def act_decrease_value(self):
        self.value = self.value - 1
        return self.value
      
    def get_value(self):
        return self.value
    
    def set_value(self,new_value):
        self.value = new_value
        return self.value

# creates a actuator class for simulation purposes 
class Actuator:
    def __init__(self,id,room,name,min,max):
        self.id = id
        self.name = name
        self.room = room
        self.state = False
        self.min = min
        self.max = max

    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

    def get_state_print(self):
        if self.state:
            return 1
        else: return 0
    
    def set_state(self,state):
        self.state = state

    def get_min(self):
        return self.min
    
    def get_max(self):
        return self.max

# creates timers for actuators and update for DB
class Timer:
    def __init__(self, waitingTime):
        self.waitingTime = waitingTime
        self.time = 0

    def checkTimer(self):
        if time.time() - self.time > self.waitingTime:
            return True
        
        return False

    def resetTimer(self):
        self.time = time.time()

    def print(self):
        print(time.time() - self.time)

class Relay:
    def __init__(self, room):
        # ATTENTION GPIO NUMBER ARE IN BCM MODE !!
        self.room = room
        self.relay_1 = 6 ## green
        self.relay_2 = 13 ## blue
        self.relay_3 = 19 ## white
        self.relay_4 = 26 ## yellow
        #...#
        GPIO.setmode(GPIO.BCM)
        #...#

    def get_room(self):
        return self.room
    
    def deafult_state(self):
        GPIO.setup(self.relay_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.relay_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.relay_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.relay_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def turn_on_relay_1(self): # then turn on
        GPIO.setup(self.relay_1, GPIO.OUT)
        GPIO.output(self.relay_1, False)

    def turn_off_relay_1(self): # and turn off
        GPIO.setup(self.relay_1, GPIO.OUT)
        GPIO.output(self.relay_1, True)

    def turn_on_relay_2(self): # then turn on
        GPIO.setup(self.relay_2, GPIO.OUT)
        GPIO.output(self.relay_2, False)

    def turn_off_relay_2(self): # and turn off
        GPIO.setup(self.relay_2, GPIO.OUT)
        GPIO.output(self.relay_2, True)
    
    def turn_on_relay_3(self): # then turn on
        GPIO.setup(self.relay_3, GPIO.OUT)
        GPIO.output(self.relay_3, False)

    def turn_off_relay_3(self): # and turn off
        GPIO.setup(self.relay_3, GPIO.OUT)
        GPIO.output(self.relay_3, True)
    
    def turn_on_relay_4(self): # then turn on
        GPIO.setup(self.relay_4, GPIO.OUT)
        GPIO.output(self.relay_4, False)

    def turn_off_relay_4(self): # and turn off
        GPIO.setup(self.relay_4, GPIO.OUT)
        GPIO.output(self.relay_4, True)


    
        
