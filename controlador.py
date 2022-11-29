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


def control_atuatores(): # todos

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
raspberry_id = 4

db_con, connection = connect(DB(None, None, None, None))
 
while contentor_ids == None:
    contentor_ids = verifica_contentor(db_con,raspberry_id)


print("Contentores: " + contentor_ids)

# Only called once
sensors = define_sensors()

# Put inside the while later
get_sensores(sensors)
time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
time_str = str(time_date)

print(sensors[0].value)

# Get to know which type of sensors are presented in each room

# while 1 :
#     get_sensores()
#     set_sensores()
#
#     control_atuatores()
    

