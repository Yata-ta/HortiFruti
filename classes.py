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



# creates a sensor class for simulation purposes 
class Sensor:
    def __init__(self,id,room, name,min,max):
        self.id = id
        self.room = room
        self.name = name
        self.value = 0
        self.min = min
        self.max = max

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id

    def get_min(self):
        return self.min
    
    def get_max(self):
        return self.max
      
    def get_value(self):
        return self.value
    
    def set_name(self):
        return self.name
    
    def set_id(self):
        return self.id

    def set_min(self):
        return self.min
    
    def set_max(self):
        return self.max
    
    def set_value(self,new_value):
        self.value = new_value
        return self.value

# creates a actuator class for simulation purposes 
class Actuator:
    def __init__(self,id,room,name,min,max):
        self.id = id
        self.room = room
        self.name = name
        self.state = 0
        self.dashboard = 0
        self.min = min
        self.max = max
        self.time_passed = 0

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def get_state(self):
        return self.state

    def get_state_print(self):
        if self.state:
            return 1
        else: return 0
    def get_min(self):
        return self.min
    
    def get_max(self):
        return self.max
    
    def set_name(self):
        return self.name
    
    def set_id(self):
        return self.id

    def set_min(self):
        return self.min
    
    def set_max(self):
        return self.max
    
    def set_value(self,new_value):
        self.value = new_value
        return self.value 
