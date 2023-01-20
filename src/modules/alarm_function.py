

def alarm_function(time_date, is_there_internet, call_number, room: int, real_values: list, limits_values: list):
    """
    Controls the room specific relays actuator based on the limits values coming from the database\n 
    [0] - Temperature in celsius\n
    [1] - Gas O2\n
    [2] - Humidity\n
    [3] - Pressure in hPa\n
    [4] - eC02 in ppm\n
    relay_module -> relay object for the specific room\n
    real_values -> list of sensor values\n
    limits_values -> list of the limits coming from the database:
    [temp_max,tem_min,hum_max,hum_min,o2_max,o2_min,Co2_max,CO2_min,press_max,press_min]
"""

    #Temperature
    if (real_values[0] >= limits_values[0] + 2):
        if (real_values[0] <= limits_values[0] + 4):
            sendSMS("HORTIFRUTI: informamos que a temperatura na camara " + str(room) + " ficou elevada: " + str(real_values[0]) + " graus.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "temperatura = "+ str(real_values[0]))
        else:
            sendSMS("HORTIFRUTI: informamos que a temperatura na camara " + str(room) + " ficou muito elevada: " + str(real_values[0]) + " graus.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "temperatura = "+ str(real_values[0]))           
    if (real_values[0] <= limits_values[1] - 2):
        if (real_values[0] >= limits_values[1] - 4):
            sendSMS("HORTIFRUTI: informamos que a temperatura na camara " + str(room) + " ficou baixa: " + str(real_values[0]) + " graus.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "temperatura = "+ str(real_values[0]))
        else:
            sendSMS("HORTIFRUTI: informamos que a temperatura na camara " + str(room) + " ficou muito baixa: " + str(real_values[0]) + " graus.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "temperatura = "+ str(real_values[0]))

    #Humidity
    humidity_var = (limits_values[2]-limits_values[3])*0.15
    if (real_values[2] >= (limits_values[2] + humidity_var)):
        if (real_values[2] <= limits_values[2] + 2*humidity_var):
            sendSMS("HORTIFRUTI: informamos que a humidade na camara " + str(room) + " ficou elevada: " + str(real_values[2]) + "%.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "humidade = "+ str(real_values[2]))
        else:
            sendSMS("HORTIFRUTI: informamos que a humidade na camara " + str(room) + " ficou muito elevada: " + str(real_values[2]) + "%.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "humidade = "+ str(real_values[2]))            
    if (real_values[2] <= (limits_values[3] - humidity_var)):
        if (real_values[2] >= limits_values[3] - 2*humidity_var):
            sendSMS("HORTIFRUTI: informamos que a humidade na camara " + str(room) + " ficou baixa: " + str(real_values[2]) + "%.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "humidade = "+ str(real_values[2]))
        else:
            sendSMS("HORTIFRUTI: informamos que a humidade na camara " + str(room) + " ficou muito baixa: " + str(real_values[2]) + "%.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "humidade = "+ str(real_values[2]))

    #O2
    O2_var = (limits_values[4]-limits_values[5])*0.15
    if (real_values[1] >= (limits_values[4] + O2_var)):
        if (real_values[1] <= (limits_values[4] + 2*O2_var)):
            sendSMS("HORTIFRUTI: informamos que a concentracao de O2 na camara " + str(room) + " ficou elevada: " + str(real_values[1]) + "%.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "concentracao de O2 = "+ str(real_values[1]))
        else:
            sendSMS("HORTIFRUTI: informamos que a concentracao de O2 na camara " + str(room) + " ficou muito elevada: " + str(real_values[1]) + "%.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "concentracao de O2 = "+ str(real_values[1]))            
    if (real_values[1] <= (limits_values[5] - O2_var)):
        if (real_values[1] >= limits_values[5] - 2*O2_var):
            sendSMS("HORTIFRUTI: informamos que a concentracao de O2 na camara " + str(room) + " ficou baixa: " + str(real_values[1]) + "%.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "concentracao de O2 = "+ str(real_values[1]))
        else:
            sendSMS("HORTIFRUTI: informamos que a concentracao de O2 na camara " + str(room) + " ficou muito baixa: " + str(real_values[1]) + "%.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "concentracao de O2 = "+ str(real_values[1]))

    #CO2
    CO2_var = (limits_values[6]-limits_values[7])*0.15
    if (real_values[4] >= (limits_values[6] + CO2_var)):
        if (real_values[4] <= (limits_values[6] + 2*CO2_var)):
            sendSMS("HORTIFRUTI: informamos que a concentracao de CO2 na camara " + str(room) + " ficou elevada: " + str(real_values[4]) + " ppm.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "concentracao de CO2 = "+ str(real_values[4]))
        else:
            sendSMS("HORTIFRUTI: informamos que a concentracao de CO2 na camara " + str(room) + " ficou muito elevada: " + str(real_values[4]) + " ppm.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "concentracao de CO2 = "+ str(real_values[4]))            
    if (real_values[4] <= (limits_values[7] - CO2_var)):
        if (real_values[4] >= limits_values[7] - 2*CO2_var):
            sendSMS("HORTIFRUTI: informamos que a concentracao de CO2 na camara " + str(room) + " ficou baixa: " + str(real_values[4]) + " ppm.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "concentracao de CO2 = "+ str(real_values[4]))
        else:
            sendSMS("HORTIFRUTI: informamos que a concentracao de CO2 na camara " + str(room) + " ficou muito baixa: " + str(real_values[4]) + " ppm.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "concentracao de CO2 = "+ str(real_values[4]))

    #Pressure
    pressure_var = (limits_values[8]-limits_values[9])*0.15
    if (real_values[3] >= (limits_values[8] + pressure_var)):
        if (real_values[3] <= (limits_values[8] + 2*pressure_var)):
            sendSMS("HORTIFRUTI: informamos que a pressao na camara " + str(room) + " ficou baixa: " + str(real_values[3]) + "hPa.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "pressao = "+ str(real_values[3]))
        else:
            sendSMS("HORTIFRUTI: informamos que a pressao na camara " + str(room) + " ficou muito baixa: " + str(real_values[3]) + "hPa.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "pressao = "+ str(real_values[3]) )        
    if (real_values[3] <= (limits_values[9] - pressure_var)):
        if (real_values[3] >= (limits_values[9] - 2*pressure_var)):
            sendSMS("HORTIFRUTI: informamos que a pressao na camara " + str(room) + " ficou baixa: " + str(real_values[3]) + "hPa.", call_number)
            #if not (is_there_internet):
            add_alarm(room, time_date, 2, "pressao = "+ str(real_values[3]))
        else:
            sendSMS("HORTIFRUTI: informamos que a pressao na camara " + str(room) + " ficou muito baixa: " + str(real_values[3]) + "hPa.", call_number)
            wait_for_A9()
            call(call_number, "../rep/bill.mp3")
            #if not (is_there_internet):
            add_alarm(room, time_date, 3, "pressao = "+ str(real_values[3]))
