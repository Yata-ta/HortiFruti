import colorama as cl
from functions import *
from simulator import *
from database import *
from db_control import *
from sensor import *

contentor_ids = None
raspberry_id = 1
sensor = []
atuadores = []
timer = []

if __name__ == '__main__':
    
    rtn = initialize_system()

    sensor = define_sensors(1)
    _,temp_max,temp_min = get_temperatura_info(sensor)



    # read temperature values
    # actuate compressor

    print(temp_max,temp_min)


    if rtn == 1:
        print("Starting local execution...")
        bme680 = initialize_sensor()
        while True:
            time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            temp = get_sensor_data(bme680)
            if (temp >= temp_max):
                print("Door Open")
            if (temp <= temp_min):
                print("Door Close")
            
            set_value_sensor(1,time_date,temp)

        #TODO code functions for local execution and execute them here.
    elif rtn == 2:
        while True:
            print(cl.Style.BRIGHT + "Want to enter developer mode and execute the simulator?(Y/N) ",end='')
            ans = str(input())
            if (ans.lower() == 'y'): 
                print(cl.Fore.YELLOW + "Starting simulator...")

                '''time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                os.system('cls||clear')
                for i in range(len(contentor_ids)):
                    sensor[i] = atualiza_sensores(contentor_ids[i], sensor[i], time_date)
                    control_atuatores(sensor[i], atuadores[i],contentor_ids[i],time_date) # falta temporização
                time.sleep(5)'''
                

                run_sim()


                break
            elif ans.lower() == 'n':
                print("Exiting program...")
                break
            else:
                print("...invalid input...")
