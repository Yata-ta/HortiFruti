
import colorama as cl
import sys
import os
from rich.traceback import install
install(show_locals=False)
import time


import modules.functions
import modules.db_control
import modules.classes
import modules.A9comm as A9comm
import simulator



alarm_pin = 25 ## red


contentor_ids = None
sensor = []
sensor_values = []
atuadores = []
timer = []

time_begin_sens = [0,0]
timing_sens = 10
timing_actu = 10
COUNTRY = "PT"
db_connected = False

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
    aux_db = modules.db_control.get_id_contentores(raspberry_id)
    if aux_db is None:
        db_connected = False
    else:
        db_connected = True


    if check_params == 3:
        modules.functions.initial_components_test(call_number)

    if rtn == 1:
        #Code functions for local execution and execute them here.


        
        print(f"Starting local execution...on room {raspberry_id}")
        modules.functions.initialize_real_sensors()
        relay_module = modules.classes.Relay(raspberry_id) # relay module of room 1
        print("Getting database information...")
        
        while contentor_ids == None:
            contentor_ids = modules.functions.verifica_contentor(raspberry_id)
        try:
            for i in range(len(contentor_ids)):
                sensor.append (modules.functions.define_sensors(contentor_ids[i],db_connected))
                atuadores.append (modules.functions.define_actuators(contentor_ids[i],db_connected))
            print("[" + cl.Fore.GREEN + "OK" + cl.Fore.WHITE + "]" + "- Connected to the database")
            old_signal = "ONLINE"
        except:
            print("[" + cl.Fore.RED + "ERROR" + cl.Fore.WHITE + "]" + "- Unable to connected to the database")
            pass

        while True:
            is_there_internet,new_signal = modules.functions.check_internet(host,old_signal,db_connected)
            old_signal = new_signal
            
            if is_there_internet is None:
                db_connected = False
            else:
                db_connected = True
            
            
            time_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            #Atuator logic function for chamber x
            #modules.functions.atuator_logic(raspberry_id,relay_module,sensor_values,limits)

            for i in range(len(contentor_ids)):
                print("\n-------   contentor: ", contentor_ids[i],"   -------")
                timing_sens, timing_actu = modules.db_control.get_timings(contentor_ids[i], timing_sens, timing_actu)
                time_begin_sens[i], sensor[i] = modules.functions.atualiza_sensores(contentor_ids[i], sensor[i], time_date, time_begin_sens[i],COUNTRY,db_connected,timing_sens)
                modules.functions.control_atuatores(sensor[i], atuadores[i],contentor_ids[i],time_date,timing_actu,relay_module,db_connected)



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

