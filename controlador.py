# import os
# import colorama as cl
# import subprocess
# import logging
# import threading
import pandas as pd
import time
from time import gmtime, strftime
from classes import *
from db import *


def define_sensors():

    sensors = []
    df_sensors = pd.read_csv('sensors.csv')

    for i in range(df_sensors.shape[0]):
        sensor_aux = Sensor(-1, contentorId, 'ini', 0, 0)

        sensor_aux.name = df_sensors.iloc[i]['Type']
        sensor_aux.value = df_sensors.iloc[i]['Current_Value']
        sensor_aux.min = df_sensors.iloc[i]['Min']
        sensor_aux.max = df_sensors.iloc[i]['Max']
        # Maybe get the id from the db
        # But it is not necessary
        # Write it later
        sensor_aux.id = df_sensors.iloc[i]['id']

        sensors.append(sensor_aux)

    return sensors

def define_actuators():

    actuators = []
    df_actuators = pd.read_csv('actuators.csv')

    for i in range(df_actuators.shape[0]):
        actuator_aux = Actuator(-1, contentorId, 'ini', 0, 0)

        actuator_aux.name = df_actuators.iloc[i]['Type']
        actuator_aux.value = df_actuators.iloc[i]['Current_Value']
        actuator_aux.min = df_actuators.iloc[i]['Min']
        actuator_aux.max = df_actuators.iloc[i]['Max']
        # Maybe get the id from the db
        # But it is not necessary
        # Write it later
        actuator_aux.id = df_actuators.iloc[i]['id']

        actuators.append(actuator_aux)

    return actuators


def atualiza_sensores(sensores):
    
    
    
    
    
    
    return 



# Get the  sensor values from the arduino
# While we don't have this ready, we will use random values
def get_sensores(sensors):  #do arduino

    for sensor in sensors:
        sensor.value = random.randint(sensor.min, sensor.max)
        print('The new value from sensor ', sensor.name,' is ', sensor.value)

    return None


# Add the sensor values to the db and also to the buffer (local memory)
def set_sensors(sensors, time):

    db_con, connection = connect(DB(None, None, None, None))

    for sensor in sensors:
        set_value_sensor(db_con, connection, sensor.id, time, sensor.value)

    # Do later the buffer part

    # Close db connection
    if connection is not None:
        connection.close()
        print('Database connection closed.')

    return

def get_atuators():  #da db

    return

def set_atuators_individual():  #para a db
    
    return


def control_atuatores(sensores, ): # todos



    for sensor_ind in sensores:
        
        if sensor_ind[0] == "temperatura":
            print("temp")
        elif sensor_ind[0] == "humidade":
            print("hum") 
        elif sensor_ind[0] == "gas 1":
            print("gas1")
        elif sensor_ind[0] == "gas 2":
            print("gas2")

    return;


def control_frigorifico():

    return;

def control_ventoina():
    return;

def control_porta():
    return;


def verifica_contentor(db, raspberry_id):
    
    PATH = './contentores_id.txt'
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        f = open('contentores_id', 'r')
        id = []
        for line in f:
            id.append(line)
        f.close()
        
        return id
    else:
         f = open('contentores_id', 'w')
         ids = get_id_contentores(db,raspberry_id)
         f.writelines(str(ids))
         f.close()
         
         return ids




contentor_ids = None
raspberry_id = 1

db_con, connection = connect(DB(None, None, None, None))
 
while contentor_ids == None:
    contentor_ids = verifica_contentor(db_con,raspberry_id)


sensor = []

# Only called once
for i in range(len(contentor_ids)):
    sensor.append (define_sensors(contentor_ids[i]))

while 1:
    for i in range(len(contentor_ids)):
        atualiza_sensores(sensor[i])
        control_atuatores(sensor[i])


