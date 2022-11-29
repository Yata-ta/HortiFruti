import colorama as cl
from functions import *
from simulator import *


rtn = initialize_system()

if rtn == 1:
    print("Starting local execution...")
    #TODO code functions for local execution and execute them here.
    
    #Ativar entrada 27
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(27, GPIO.OUT)
    #time.sleep(2)
    #GPIO.output(27, GPIO.LOW)
    
    #ser = serial.Serial('/dev/ttyACM0', 14400, timeout=1)
    #ser.reset_input_buffer()
    
    #while True:
    #    try:
    #        if ser.in_waiting > 0:
    #            line = ser.read(ser.inWaiting()).decode('utf-8')
    #            print(line)
    #            time.sleep(1)
    #    except UnicodeDecodeError:
    #        pass
            
    
    #Rasp controll
    hum_timer = Timer(60)
    send_data_timer = Timer(120)
    
    #Base de dados
    contentorId = '1'
    db_con, connection = connect(DB(None, None, None, None))
    fruta, utilizadorid = identificacao(db_con, contentorId)
    
    tipo1_sensors, valor1_sensors = get_value_sensores(db_con, contentorId)
    sensorsId1 = get_id_sensor(db_con, contentorId)

    tipo1_actuator, valor1_actuator = get_value_atuadores(db_con, contentorId)
    actuatorsId1 = get_id_atuador(db_con, contentorId)

    # Create actuators for the main loop
    actuators = create_actuators(tipo1_actuator)

    #client = Client()
    temp, hum, co2, o2 = 15, 85, 30, 10

    while (1):
        time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        #temp, hum, co2, o2, press = client.readMeasures()
        sensors = [hum, temp, co2, o2]

        tipo1_actuator, valor1_actuator = get_value_atuadores(db_con, contentorId)

        auxiliar_control(actuators, sensors, valor1_actuator, hum_timer)
   
        if send_data_timer.checkTimer():
            send_history_sensors(db_con, connection, sensorsId1, str(time_date), sensors)
            send_history_actuators(db_con, connection, actuatorsId1, str(time_date), actuators)
            send_data_timer.resetTimer()

        send_values_sensores(db_con, connection, contentorId, tipo1_sensors, sensors)
 

        # print("Tempo:", time.time()- ini)
        # print(actuators[1].get_name()," state:", actuators[1].get_state_1_0())
        # print(actuators[0].get_name()," state:", actuators[0].get_state_1_0())
        # Clear terminal for better reading
        time.sleep(1)
        os.system('cls')
        # os.system('clear') #on Linux System

    #client.close()
elif rtn == 2:
    while True:
        print(cl.Style.BRIGHT + "Want to enter developer mode and execute the simulator?(Y/N) ",end='')
        ans = str(input())
        if (ans.lower() == 'y'): 
            print(cl.Fore.YELLOW + "Starting simulator...")
            run_sim()
            break
        elif ans.lower() == 'n':
            print("Exiting program...")
            break
        else:
            print("...invalid input...")
