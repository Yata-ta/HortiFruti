
import colorama as cl
import sys
import os



import modules.db_control
import modules.database 
import modules.functions
import modules.classes
import modules.A9comm as A9comm
import simulator

alarm_pin = 25 ## red

COUNTRY = "PT"

contentor_ids = None
raspberry_id = 1
sensor = []
sensor_values = []
atuadores = []
timer = []

call_number = "+351910649345"

if __name__ == '__main__':

    check_params = modules.functions.start(sys.argv)

    if check_params == 2 or check_params== None:
        sys.exit(0)
    
    rtn = modules.functions.initialize_system()

    #modules.functions.initial_components_test()

    sensor = modules.db_control.define_sensors(1)
    _,temp_max,temp_min = modules.db_control.get_temperatura_info(sensor)
    _,o2_max,o2_min = modules.db_control.get_o2_info(sensor)
    _,co2_max,co2_min = modules.db_control.get_co2_info(sensor)
    _,hum_max,hum_min = modules.db_control.get_hum_info(sensor)
    _,pressao_max,pressao_min = modules.db_control.get_pressao_info(sensor)

    A9comm.call(call_number)
    

    if rtn == 1:
        #TODO code functions for local execution and execute them here.

        print("Starting local execution...")
        modules.functions.initialize_real_sensors()
        relay_module = modules.classes.Relay(1) # relay module of room 1

        while True:

            time_date = modules.database.strftime("%Y-%m-%d %H:%M:%S", modules.database.gmtime())
            # read temperature values
            sensor_values = modules.functions.read_real_sensors(COUNTRY)

            #print(f"CO2: {sensor_values[4]}")
            #print(f"Humidity: {sensor_values[2]}")
            print("-------")
            print()
            print(f"TEMP: {temp_min} < {sensor_values[0]:.2f} < {temp_max}")
            print(f"O2: {o2_min} < {modules.functions.get_OxygenValues():.2f} < {o2_max}")
            print(f"CO2: {co2_min} < {sensor_values[4]:.2f} < {co2_max}")
            print(f"HUM: {hum_min} < {sensor_values[2]:.2f} < {hum_max}")
            print(f"PRESSAO: {pressao_min} < {sensor_values[3]:.2f} < {pressao_max}")
            print()
            print("-------")

            data = [f"{sensor_values[0]:.2f}",f"{modules.functions.get_OxygenValues():.2f}"]
            modules.functions.log_data(data)

            #TODO create atuator logic function in functions...

            if (sensor_values[0] >= temp_max):
                ## Make the room colder --> turn on frizzer
                relay_module.turn_on_relay_2()
                pass
                
            if (sensor_values[0] <= temp_min):
                ## temperature too low --> turn off frizzer
                relay_module.turn_off_relay_2()
                pass
            
            if f"{time_date[17]}{time_date[18]}" == "59": ## test alarm led 
                modules.functions.alarm(alarm_pin,"on")

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

