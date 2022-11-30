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




def define_sensors(contentorId):

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

def define_actuators(contentorId):

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


    

def control_atuatores(sensores, atuadores,contentorid): # todos


    for atuador in atuadores:
        
        if(atuador.name == "Frigorifico"):
                nivel = get_nivel_regra(atuador.id)
                control_frigorifico(sensores,nivel,atuador)
                
        if(atuador.name == "Ventoinha"):
                nivel = get_nivel_regra(atuador.id)
                control_ventoinha(sensores,nivel,atuador)
    for atuador in atuadores:      
             
        if(atuador.name == "Porta"):
                nivel = get_nivel_regra(atuador.id)
                control_porta(sensores,nivel,atuador,contentorid)

    return

def get_temperatura_info(sensores):
    #print("get_temp_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "temperatura"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
        
    return None, None, None

def get_CO2_info(sensores):
    #print("get_CO2_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "CO2"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
       
    return None, None, None

def get_O2_info(sensores):
    #print("get_O2_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "O2"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
        
    return None, None, None

def get_humidade_info(sensores):
    #print("get_HUM_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "humidade"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
        
    return None, None, None

def muda_frigorifico(valor, atuador):
   # get_specific_value_atuador
    #manda comando pro arduino
    print(atuador.name, "mudou para ", valor)
    return

def muda_ventoinha(valor, atuador):
    #manda comando pro arduino
    print(atuador.name, "mudou para ", valor)
    return

def muda_porta(valor, atuador):
    #manda comando pro arduino
    print(atuador.name, "mudou para ", valor)
    return

def control_frigorifico(sensores, nivel, atuador):
    
    temp, max_, min = get_temperatura_info(sensores)
    if(nivel == 0):         # quem manda é a raspberry
        if(temp > max_):
            muda_frigorifico(1,atuador)
        elif(temp < min):
            muda_frigorifico(0,atuador)
    elif(nivel != 0):
        muda_frigorifico(max(nivel,0),atuador)

    return

def control_ventoinha(sensores, nivel, atuador):
    CO2, max_1, min_1 = get_CO2_info(sensores)
    O2, max_2, min_2 = get_O2_info(sensores)

    if(nivel == 0):         # quem manda é a raspberry
        if(CO2 > max_1 or O2 > max_2):               # falta aqui hierarquia. quem manda?? CO2, O2, o minimo ou o maximo??
            muda_ventoinha(1,atuador)
        elif(CO2 < min_1 or O2 < min_2):
            muda_ventoinha(0,atuador)
    elif(nivel != 0):
        muda_ventoinha(max(nivel,0),atuador)
    return

def control_porta(sensores, nivel, atuador, contentorid):
    ventoinha = get_specific_value_atuador(str(contentorid), "Ventoinha",None)
    hum, max_, min = get_humidade_info(sensores)
    if(nivel == 0):         # quem manda é a raspberry
        if(hum > max_ or ventoinha == 1):
            muda_porta(1,atuador)
        elif(hum < min and ventoinha == 0):
            muda_porta(0,atuador)
    elif(nivel != 0):
        muda_porta(max(nivel,0),atuador)

    return


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



#                           Main

contentor_ids = None
raspberry_id = 1

db_con, connection = connect(DB(None, None, None, None))
 
while contentor_ids == None:
    contentor_ids = verifica_contentor(db_con,raspberry_id)


sensor = []
atuadores = []
timer = []

# Only called once
for i in range(len(contentor_ids)):
    sensor.append (define_sensors(contentor_ids[i]))
    atuadores.append (define_actuators(contentor_ids[i]))

    
while 1:
                # limpar terminal
    os.system('cls||clear')
    
    for i in range(len(contentor_ids)):
       atualiza_sensores(sensor[i])
       control_atuatores(sensor[i], atuadores[i],contentor_ids[i]) # falta temporização

       time.sleep(1)

    
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


# def define_sensors(contentorId):
#
#     sensors = []
#     df_sensors = pd.read_csv('sensors.csv')
#
#     for i in range(df_sensors.shape[0]):
#         sensor_aux = Sensor(-1, contentorId, 'ini', 0, 0)
#
#         sensor_aux.name = df_sensors.iloc[i]['Type']
#         sensor_aux.value = df_sensors.iloc[i]['Current_Value']
#         sensor_aux.min = df_sensors.iloc[i]['Min']
#         sensor_aux.max = df_sensors.iloc[i]['Max']
#         # Maybe get the id from the db
#         # But it is not necessary
#         # Write it later
#         sensor_aux.id = df_sensors.iloc[i]['id']
#
#         sensors.append(sensor_aux)
#
#     return sensors

def define_sensors(contentorId):

    sensors = []

    # Open db connection
    db_con, connection = connect(DB(None, None, None, None))

    sensors_db = get_value_sensores(db_con, contentorId)

    print(sensors_db)

    for i in range(len(sensors_db)):
        sensor_aux = Sensor(-1, contentorId, 'ini', 0, 0)

        sensor_aux.id = sensors_db[i][0]
        sensor_aux.name = sensors_db[i][1]
        sensor_aux.value = sensors_db[i][2]
        sensor_aux.max = sensors_db[i][4]
        sensor_aux.min = sensors_db[i][5]

        sensors.append(sensor_aux)

    # Close db connection
    if connection is not None:
        connection.close()
        print('Database connection closed.')

    return sensors


# def define_actuators(contentorId):
#
#     actuators = []
#     df_actuators = pd.read_csv('actuators.csv')
#
#     for i in range(df_actuators.shape[0]):
#         actuator_aux = Actuator(-1, contentorId, 'ini', 0, 0)
#
#         actuator_aux.name = df_actuators.iloc[i]['Type']
#         actuator_aux.value = df_actuators.iloc[i]['Current_Value']
#         actuator_aux.min = df_actuators.iloc[i]['Min']
#         actuator_aux.max = df_actuators.iloc[i]['Max']
#         # Maybe get the id from the db
#         # But it is not necessary
#         # Write it later
#         actuator_aux.id = df_actuators.iloc[i]['id']
#
#         actuators.append(actuator_aux)
#
#     return actuators

def define_actuators(contentorId):

    actuators = []

    # Open db connection
    db_con, connection = connect(DB(None, None, None, None))

    actuators_db = get_value_atuadores(db_con, contentorId)

    print(actuators_db)

    for i in range(len(actuators_db)):
        actuator_aux = Actuator(-1, contentorId, 'ini', 0, 0)

        actuator_aux.id = actuators_db[i][0]
        actuator_aux.name = actuators_db[i][1]
        actuator_aux.value = actuators_db[i][2]
        actuator_aux.dashboard = actuators_db[i][4]

        actuators.append(actuator_aux)

    # Close db connection
    if connection is not None:
        connection.close()
        print('Database connection closed.')

    return actuators


def atualiza_sensores(contentorId, sensors, time):

    try:
        sensors = define_sensors(contentorId)
    except:
        print('Could not connect with the db')

    sensors = get_sensors(sensors)

    try:
        set_sensors(sensors, time)
    except:
        print('Could not connect with the db')

    return sensors

# Get the  sensor values from the arduino
# While we don't have this ready, we will use random values
def get_sensors(sensors):  #do arduino

    for sensor in sensors:
        sensor.value = random.randint(sensor.min, sensor.max)
        print('The new value from sensor ', sensor.name,' is ', sensor.value)

    return sensors


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

def get_actuators():  #da db

    return

def set_actuators_individual(actuator, time):  #para a db

    db_con, connection = connect(DB(None, None, None, None))

    set_value_atuador(db_con, connection, actuator.id, time, actuator.value)

    # Do later the buffer part
    # Close db connection
    if connection is not None:
        connection.close()
        print('Database connection closed.')

    return None


def control_atuatores(sensores, actuators, time): # todos



    for sensor_ind in sensores:
        
        if sensor_ind[0] == "temperatura":
            print("temp")
        elif sensor_ind[0] == "humidade":
            print("hum") 
        elif sensor_ind[0] == "gas 1":
            print("gas1")
        elif sensor_ind[0] == "gas 2":
            print("gas2")

    for actuator in actuators:
        current_actuator_value = random.randint(0, 1)
        print('The value from actuator ', actuator.name,' is ', actuator.value)

        if current_actuator_value != actuator.value:
            actuator.value = current_actuator_value
            set_actuators_individual(actuator, time)

    return


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

time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

sensors = define_sensors(contentor_ids[0])

actuators = define_actuators(contentor_ids[0])

atualiza_sensores(contentor_ids[0], sensors, time_date)

# # Only called once
# for i in range(len(contentor_ids)):
#     sensor.append (define_sensors(contentor_ids[i]))
#
# while 1:
#     for i in range(len(contentor_ids)):
#         atualiza_sensores(sensor[i])
#         control_atuatores(sensor[i])
#
#


