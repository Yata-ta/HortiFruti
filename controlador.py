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



# Get the  sensor values from the arduino
# While we don't have this ready, we will use random values

def get_sensors(sensors):  #do arduino

      
    for sensor in sensors:
        sensor.value = random.randint(sensor.min-50, sensor.max+50)
        print('The new value from sensor ', sensor.name,' is ', sensor.value)
    return  sensors

def send_db_sensor_buffer():
    if db_connected is True:
        data_df = pd.read_csv('sensor_data.csv')

        range_for = min(20, data_df.shape[0])

        for i in range(range_for):

            print(i)

            id = data_df.iloc[0]['id']
            time = data_df.iloc[0]['Time']
            value = data_df.iloc[0]['Value']
            set_value_sensor(id, time, value)

            print(id, time, value)

            data_df.drop(data_df.index[0], axis=0, inplace=True)

        data_df.to_csv('sensor_data.csv', index=False)

    return

def send_db_actuator_buffer():
    if db_connected is True:
        data_df = pd.read_csv('actuator_data.csv')

        range_for = min(20, data_df.shape[0])

        for i in range(range_for):

            print(i)

            id = data_df.iloc[0]['id']
            time = data_df.iloc[0]['Time']
            value = data_df.iloc[0]['Value']
            set_value_atuador(id, time, value)

            print(id, time, value)

            data_df.drop(data_df.index[0], axis=0, inplace=True)

        data_df.to_csv('actuator_data.csv', index=False)

    return

def define_sensors(contentorId):
    sensors = []
    data_df = []

    if db_connected is True:

        # Open db connection
        sensors_db = get_value_sensores(contentorId)

        for i in range(len(sensors_db)):
            sensor_aux = Sensor(-1, contentorId, 'ini', 0, 0)

            sensor_aux.id = sensors_db[i][0]
            sensor_aux.name = sensors_db[i][1]
            sensor_aux.value = sensors_db[i][2]
            sensor_aux.max = sensors_db[i][4]
            sensor_aux.min = sensors_db[i][5]

            sensors.append(sensor_aux)
            data_df.append([sensor_aux.name, sensor_aux.id, sensor_aux.value, sensor_aux.min, sensor_aux.max])

        df_sensors = pd.DataFrame(data_df, columns=['Type','id','Current_Value','Min','Max'])
        df_sensors.to_csv("sensors.csv")

        return sensors

    else:
        df_sensors = pd.read_csv('sensors.csv')

        for i in range(df_sensors.shape[0]):
            sensor_aux = Sensor(-1, contentorId, 'ini', 0, 0)

            sensor_aux.name = df_sensors.iloc[i]['Type']
            sensor_aux.value = df_sensors.iloc[i]['Current_Value']
            sensor_aux.min = df_sensors.iloc[i]['Min']
            sensor_aux.max = df_sensors.iloc[i]['Max']
            sensor_aux.id = df_sensors.iloc[i]['id']

            sensors.append(sensor_aux)

        return sensors

    # Add the sensor values to the db and also to the buffer (local memory)
def set_sensors(sensors, time_day,temp_sens_passado):
  
  if(timing_sens < time.time() - temp_sens_passado): 

    if db_connected is True:

        for sensor in sensors:
            set_value_sensor(sensor.id, time_day, sensor.value)
        temp_sens_passado = time.time()
        

    # buffer part
    else:
        df_data = pd.read_csv('sensor_data.csv')

        for sensor in sensors:
            row = [sensor.id, time_day, sensor.value]
            df_data.loc[len(df_data)] = row

        df_data.to_csv('sensor_data.csv', index=False)
        temp_sens_passado = time.time()
        

    print("--- Mandou Para a DB ---") 

  return temp_sens_passado



def atualiza_sensores(contentorId, sensors, time, temp_sens_passado):

    try:
        sensors = define_sensors(contentorId)
    except:
        print('Could not connect with the db')

    sensors = get_sensors(sensors)

    #try:
    temp_sens_passado = set_sensors(sensors, time,temp_sens_passado)
    #except:
    #    print('Could not connect with the db')

    return temp_sens_passado, sensors

def define_actuators(contentorId):
    actuators = []
    data_df = []

    if db_connected is True:

        # Open db connection
        actuators_db = get_value_atuadores(contentorId)

        for i in range(len(actuators_db)):
            actuator_aux = Actuator(-1, contentorId, 'ini', 0, 0)

            actuator_aux.id = actuators_db[i][0]
            actuator_aux.name = actuators_db[i][1]
            actuator_aux.value = actuators_db[i][2]
            actuator_aux.dashboard = actuators_db[i][4]
            actuator_aux.time_passed = 0
            actuators.append(actuator_aux)
            data_df.append([actuator_aux.name, actuator_aux.id, actuator_aux.value, actuator_aux.dashboard])

        df_actuators = pd.DataFrame(data_df, columns=['Type','id','Current_Value','dashboard'])
        df_actuators.to_csv("actuators.csv")

        return actuators

    else:
        df_actuators = pd.read_csv('actuators.csv')

        for i in range(df_actuators.shape[0]):
            actuator_aux = Actuator(-1, contentorId, 'ini', 0, 0)

            actuator_aux.name = df_actuators.iloc[i]['Type']
            actuator_aux.value = df_actuators.iloc[i]['Current_Value']
            actuator_aux.id = df_actuators.iloc[i]['id']
            actuator_aux.dashboard = df_actuators[i]['dashboard']
            actuator_aux.time_passed = 0
            actuators.append(actuator_aux)

        return actuators





def control_atuatores(sensores, atuadores,contentorid,time): # todos

    try:
        atuadores = define_actuators(contentorid)
    except:
        print('Could not connect with the db')

    for atuador in atuadores:
        
        if(atuador.name == "Frigorifico"):
                # nivel = get_nivel_regra(atuador.id)
                nivel = atuador.dashboard
                control_frigorifico(sensores,nivel,atuador,time)
                
        if(atuador.name == "Ventoinha"):
                # nivel = get_nivel_regra(atuador.id)
                nivel = atuador.dashboard
                control_ventoinha(sensores,nivel,atuador,time)
    for atuador in atuadores:      
             
        if(atuador.name == "Porta"):
                # nivel = get_nivel_regra(atuador.id)
                nivel = atuador.dashboard
                control_porta(sensores,nivel,atuador,contentorid,time)

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

def add_actuator_data_buffer(value, actuator, time):

    df_data = pd.read_csv('actuator_data.csv')

    row = [actuator.id, time, value]
    df_data.loc[len(df_data)] = row

    df_data.to_csv('actuator_data.csv', index=False)
    return

def muda_frigorifico(valor, atuador, time):
    # get_specific_value_atuador
    # manda comando pro arduino
    if db_connected is True:
        set_value_atuador(atuador.id, time, valor)

    else:
        add_actuator_data_buffer(valor, atuador, time)

    print(atuador.name, "mudou para ", valor)
    return


def muda_ventoinha(valor, atuador, time):
    # manda comando pro arduino
    if db_connected is True:
        set_value_atuador(atuador.id, time, valor)
    else:
        add_actuator_data_buffer(valor, atuador, time)

    print(atuador.name, "mudou para ", valor)
    return


def muda_porta(valor, atuador, time):
    # manda comando pro arduino
    if db_connected is True:
        set_value_atuador(atuador.id, time, valor)
    else:
        add_actuator_data_buffer(valor, atuador, time)
    print(atuador.name, "mudou para ", valor)
    return

def control_frigorifico(sensores, nivel, atuador,time_day):
    
    temp, max_, min = get_temperatura_info(sensores)
    if(nivel == 0):         # quem manda é a raspberry
      if(timing_actu < time.time() - atuador.time_passed): 
        if(temp > max_):
            muda_frigorifico(1,atuador,time_day)
            atuador.time_passed = time.time()
        elif(temp < min):
            muda_frigorifico(0,atuador,time_day)
            atuador.time_passed = time.time()
    elif(nivel != 0):
        muda_frigorifico(max(nivel,0),atuador,time_day)

    return

def control_ventoinha(sensores, nivel, atuador,time_day):
    CO2, max_1, min_1 = get_CO2_info(sensores)
    O2, max_2, min_2 = get_O2_info(sensores)

    if(nivel == 0):         # quem manda é a raspberry
      if(timing_actu < time.time() - atuador.time_passed): 

        if(CO2 > max_1 or O2 > max_2):               # falta aqui hierarquia. quem manda?? CO2, O2, o minimo ou o maximo??
            muda_ventoinha(1,atuador,time_day)
            atuador.time_passed = time.time()

        elif(CO2 < min_1 or O2 < min_2):
            muda_ventoinha(0,atuador,time_day)
            atuador.time_passed = time.time()

    elif(nivel != 0):
        muda_ventoinha(max(nivel,0),atuador,time_day)
    
    return

def control_porta(sensores, nivel, atuador, contentorid,time_day):
    ventoinha = get_specific_value_atuador(str(contentorid), "Ventoinha",None)
    hum, max_, min = get_humidade_info(sensores)
    if(nivel == 0):         # quem manda é a raspberry
      if(timing_actu < time.time() - atuador.time_passed): 
        if(hum > max_ or ventoinha == 1):
            muda_porta(1,atuador,time_day)
            atuador.time_passed = time.time()
        elif(hum < min and ventoinha == 0):
            muda_porta(0,atuador,time_day)
            atuador.time_passed = time.time()
    elif(nivel != 0):
        muda_porta(max(nivel,0),atuador,time_day)

    return


def verifica_contentor( raspberry_id):
    
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
         ids = get_id_contentores(raspberry_id)
         f.writelines(str(ids))
         f.close()
         
         return ids


    

#                           Main

contentor_ids = None
raspberry_id = 1
time_begin_sens = [0,0]
timing_sens = 10
timing_actu = 10

global db_connected
aux_db = get_id_contentores(raspberry_id)
if aux_db is None:
    db_connected = False
else:
    db_connected = True
 
while contentor_ids == None:
    contentor_ids = verifica_contentor(raspberry_id)


sensor = []
atuadores = []
timer = []

# Only called once
for i in range(len(contentor_ids)):
    sensor.append (define_sensors(contentor_ids[i]))
    atuadores.append (define_actuators(contentor_ids[i]))

    
while 1:
                # limpar terminal
   # os.system('cls||clear')

    aux_db = get_id_contentores(raspberry_id)
    if aux_db is None:
        db_connected = False
    else:
        db_connected = True
        send_db_sensor_buffer()
        send_db_actuator_buffer()

    time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    for i in range(len(contentor_ids)):
        print("\n-------   contentor: ", contentor_ids[i],"   -------")
        timing_sens, timing_actu = get_timings(contentor_ids[i], timing_sens, timing_actu)
        time_begin_sens[i], sensor[i] = atualiza_sensores(contentor_ids[i], sensor[i], time_date, time_begin_sens[i])
        control_atuatores(sensor[i], atuadores[i],contentor_ids[i],time_date)
    time.sleep(2)
       
