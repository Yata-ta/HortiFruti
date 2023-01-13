from .database import * 
from .classes import * 

def define_sensors(contentorId: int) -> list:

    sensors = []

    # Open db connection

    sensors_db = get_value_sensores( contentorId)


    for i in range(len(sensors_db)):
        sensor_aux = Sensor(-1, contentorId, 'ini', 0, 0)

        sensor_aux.id = sensors_db[i][0]
        sensor_aux.name = sensors_db[i][1]
        sensor_aux.value = sensors_db[i][2]
        sensor_aux.max = sensors_db[i][4]
        sensor_aux.min = sensors_db[i][5]

        sensors.append(sensor_aux)

    
    return sensors

def get_temperatura_info(sensores):
    #print("get_temp_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "temperatura"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min

def get_o2_info(sensores):
    #print("get_temp_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "O2"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min

def get_co2_info(sensores):
    #print("get_temp_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "CO2"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min

def get_hum_info(sensores):
    #print("get_temp_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "humidade"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min

def get_pressao_info(sensores):
    #print("get_temp_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "pressao"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min

 