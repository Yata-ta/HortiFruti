import colorama as cl
import sys
import os


import modules.db_control
import modules.database 
import modules.functions
import simulator

contentor_ids = None
raspberry_id = 1
sensor = []
atuadores = []
timer = []

if __name__ == '__main__':

    check_params = modules.functions.start(sys.argv)

    if check_params == 2 or check_params== None:
        sys.exit(0)
    
    rtn = modules.functions.initialize_system()

    sensor = modules.db_control.define_sensors(1)
    _,temp_max,temp_min = modules.db_control.get_temperatura_info(sensor)
    

    if rtn == 1:
        #TODO code functions for local execution and execute them here.

        print("Starting local execution...")
        modules.functions.initialize_real_sensors()

        while True:

            time_date = modules.database.strftime("%Y-%m-%d %H:%M:%S", modules.database.gmtime())
            # read temperature values
            temp_value,gas_value,humidity_value,pressure_value = modules.functions.read_real_sensors("PT")

            print(f"{temp_min} < {temp_value:.2f} < {temp_max}")

            if (temp_value >= temp_max):
                modules.functions.print_y("Door Open")
            if (temp_value <= temp_min):
                modules.functions.print_y("Door Close")
            
             # SAFETY DEBUG MODE, TO NOT FLOOD THE DATABASE
            if check_params == 1:
                modules.db_control.set_value_sensor(1,time_date,temp_value)

    elif rtn == 2:
        while True:
            print(cl.Style.BRIGHT + "Want to enter developer mode and execute the simulator?(Y/N) ",end='')
            ans = str(input())
            if (ans.lower() == 'y'): 
                print(cl.Fore.YELLOW + "Starting simulator...")
                simulator.run_sim()
                break
            elif ans.lower() == 'n':
                print("Exiting program...")
                break
            else:
                print("...invalid input...")
