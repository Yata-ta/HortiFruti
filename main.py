import colorama as cl
from functions import *
from simulator import *
from database import *
from db_control import *

contentor_ids = None
raspberry_id = 1
sensor = []
atuadores = []
timer = []

if __name__ == '__main__':
    
    rtn = initialize_system()

    sensor = define_sensors(1)
    _,temp_max,temp_min = get_temperatura_info(sensor)

    # actuate compressor

    print(temp_max,temp_min)


    if rtn == 1:
        #TODO code functions for local execution and execute them here.

        print("Starting local execution...")
        while True:

            time_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            # read temperature values
            temp_value,gas_value,humidity_value,pressure_value = initialize_real_sensors("PT")

            print(f"{temp_min} < {temp_value} < {temp_max}")

            if (temp_value >= temp_max):
                print_y("Door Open")
            if (temp_value <= temp_min):
                print_y("Door Close")
            
            set_value_sensor(1,time_date,temp_value)

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
