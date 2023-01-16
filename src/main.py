
import colorama as cl
import sys
import os
from rich.traceback import install
install(show_locals=False)



import modules.functions
import modules.db_control
import modules.database 
import modules.classes
import modules.A9comm as A9comm
import simulator

alarm_pin = 25 ## red

COUNTRY = "PT"

contentor_ids = None
sensor = []
sensor_values = []
atuadores = []
timer = []

call_number = "+351910649345"

host = "1.1.1.1" # local DNS server

if __name__ == '__main__':

    check_params = modules.functions.start(sys.argv)

    if check_params == 2 or check_params== None:
        sys.exit(0)
    
    rtn = modules.functions.initialize_system()

    #TODO retrive rooms (rapsberry_id) id from the database
    #using 1 for now..
    raspberry_id = 1

    if check_params == 3:
        modules.functions.initial_components_test(call_number)

    if rtn == 1:
        #Code functions for local execution and execute them here.

        print(f"Starting local execution...on room {raspberry_id}")
        modules.functions.initialize_real_sensors()
        relay_module = modules.classes.Relay(raspberry_id) # relay module of room 1
        print("Getting database information...")
        try:
            sensor = modules.db_control.define_sensors(raspberry_id)
            print("[" + cl.Fore.GREEN + "OK" + cl.Fore.WHITE + "]" + "- Connected to the database")
            old_signal = "ONLINE"
        except:
            print("[" + cl.Fore.RED + "ERROR" + cl.Fore.WHITE + "]" + "- Unable to connected to the database")
            pass
        try:
            _,temp_max,temp_min = modules.db_control.get_temperatura_info(sensor)
            _,o2_max,o2_min = modules.db_control.get_o2_info(sensor)
            _,co2_max,co2_min = modules.db_control.get_co2_info(sensor)
            _,hum_max,hum_min = modules.db_control.get_hum_info(sensor)
            _,pressao_max,pressao_min = modules.db_control.get_pressao_info(sensor)
            print("[" + cl.Fore.GREEN + "OK" + cl.Fore.WHITE + "]" + "- Obtained sensor limits")
            limits = [temp_max,temp_min,hum_max,hum_min,o2_max,o2_min,co2_max,co2_min,pressao_max,pressao_min]
        except:
            print("[" + cl.Fore.RED + "ERROR" + cl.Fore.WHITE + "]" + "- Unable to obtain sensor limits...raising alarm")
            modules.functions.alarm(alarm_pin,"on")

        print("Everything is" + cl.Fore.GREEN + " OK " + cl.Fore.WHITE +"starting main loop")
        while True:

            # Test internet connection
            is_there_internet,new_signal = modules.functions.check_internet(host,old_signal)
            old_signal = new_signal

            time_date = modules.database.strftime("%Y-%m-%d %H:%M:%S", modules.database.gmtime())
            # read sensor values
            sensor_values = modules.functions.read_real_sensors(COUNTRY)


            print("-------")
            print()
            print(f"TEMP: {temp_min} < {sensor_values[0]:.2f} < {temp_max}")
            print(f"O2: {o2_min} < {modules.functions.get_OxygenValues():.2f} < {o2_max}")
            print(f"CO2: {co2_min} < {sensor_values[4]:.2f} < {co2_max}")
            print(f"HUM: {hum_min} < {sensor_values[2]:.2f} < {hum_max}")
            print(f"PRESSAO: {pressao_min} < {sensor_values[3]:.2f} < {pressao_max}")
            print(f"internet status: {is_there_internet}")
            print()
            print("-------")

            #Atuator logic function for chamber x
            modules.functions.atuator_logic(raspberry_id,relay_module,sensor_values,limits)

            if (is_there_internet): # there is no internet log the data and signal OFFLINE
                #[time;temp;hum;o2;co2;press;k1;k3;k5;k7]
                sensor_data = [f"{sensor_values[0]:.2f}",f"{sensor_values[2]:.2f}",f"{modules.functions.get_OxygenValues():.2f}",f"{sensor_values[4]:.2f}",f"{sensor_values[3]:.2f}"]
                actuator_data = relay_module.get_states()
                modules.functions.log_data(sensor_data,actuator_data)
                pass

             # SAFETY DEBUG MODE, TO NOT FLOOD THE DATABASE
            if check_params == 1:
                modules.db_control.set_value_sensor(5,time_date,sensor_values[0])
                modules.db_control.set_value_sensor(6,time_date,sensor_values[2])
                modules.db_control.set_value_sensor(7,time_date,sensor_values[4])
                modules.db_control.set_value_sensor(8,time_date,modules.functions.get_OxygenValues())
                modules.db_control.set_value_sensor(9,time_date,sensor_values[3])


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

