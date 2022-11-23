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

# Creates de client for comunication with the server 
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

# Server class which will output information form the simulator
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
    def __init__(self,name,min,max):
        self.name = name
        self.value = 0
        self.min = min
        self.max = max

    def get_name(self):
        return self.name

    def start_increase_value(self):
        #self.value = r.gauss(self.max,self.min)
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
    def __init__(self,name,min,max):
        self.name = name
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
