## *************************************** ##
        ## Function Repository file ##
## *************************************** ##
## ** Created by Gabriel Pizzighini and ... ** ## 

import os
import colorama as cl
import subprocess
import logging
import threading
import time
from classes import *

# prints error [local]
def print_r(str):
    print(cl.Back.RED + str)

# prints in yellow [local]
def print_y(str):
    print(cl.Fore.YELLOW + str)

# print for the chamber simulator
def print_chamber(sensors_names,values,actuators_names,act_values):
    print(cl.Style.BRIGHT + "     ----------------------------- CHAMBER ------------------------------")
    print(f"                              "+cl.Style.BRIGHT + cl.Fore.BLACK +cl.Back.YELLOW + f"Time : {values[0]}",end='')
    print("                               ")
    if act_values[0] == 1:
        print(cl.Fore.YELLOW + f"                 {sensors_names[0]} : {values[1]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[0]} : " +cl.Back.GREEN + "ON")
    elif act_values[0] == 0:
        print(cl.Fore.YELLOW + f"                 {sensors_names[0]} : {values[1]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[0]} : " +cl.Back.RED + "OFF")
    if act_values[1] == 1:
        print(cl.Fore.LIGHTBLUE_EX  + f"                    {sensors_names[1]} : {values[2]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[1]} : " +cl.Back.GREEN + "ON")
    elif act_values[1] == 0:
        print(cl.Fore.LIGHTBLUE_EX  + f"                    {sensors_names[1]} : {values[2]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[1]} : " +cl.Back.RED + "OFF")
    if act_values[2] == 1:
        print(cl.Fore.MAGENTA + f"                         {sensors_names[2]} : {values[3]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.GREEN + "ON")
    elif act_values[2] == 0:
        print(cl.Fore.MAGENTA + f"                         {sensors_names[2]} : {values[3]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.RED + "OFF")
    if act_values[3] == 1:
        print(cl.Fore.CYAN + f"                          {sensors_names[3]} : {values[4]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.GREEN + "ON")
    elif act_values[3] == 0:
        print(cl.Fore.CYAN + f"                          {sensors_names[3]} : {values[4]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[2]} : " +cl.Back.RED + "OFF")
    if act_values[4] == 1:
        print(cl.Fore.RED + f"                    {sensors_names[4]} : {values[5]:.2f}  " + cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[3]} : " +cl.Back.GREEN + "ON")
    elif act_values[4] == 0:
        print(cl.Fore.RED + f"                    {sensors_names[4]} : {values[5]:.2f}  "+ cl.Fore.WHITE +"||" + cl.Fore.WHITE + f"  {actuators_names[3]} : " +cl.Back.RED + "OFF")
    print(cl.Style.BRIGHT + "     ------------------------- CTRL + C TO EXIT -------------------------")
    print(cl.Style.RESET_ALL)

# create simulated sensors
def create_sensors(names):
    Temperature_sensor = Sensor(name=names[0],min=12,max=24)
    Humidity_sensor = Sensor(name=names[1],min=10,max=80)
    CO2_sensor = Sensor(name=names[2],min=20,max=30)
    O2_sensor = Sensor(name=names[3],min=0.5,max=1)
    Pressure_sensor =  Sensor(name=names[4],min=10,max=20)

    # if needed add more sensors HERE:

    return Temperature_sensor, Humidity_sensor, CO2_sensor , O2_sensor, Pressure_sensor

def start_simulation(names,size):
    cl.init(autoreset=True)
    var = 0
    # Create sensors for the main loop
    Temp_sensor, Hum_sensor, CO2_sensor , O2_sensor, Press_sensor = create_sensors(names)
    while (var < size):
        t = dt.datetime.now().strftime('%M:%S.%f')

        # generate gauss values
        Temp_sensor.generate_value()
        Hum_sensor.generate_value()
        CO2_sensor.generate_value()
        O2_sensor.generate_value()
        Press_sensor.generate_value()

        # If you want to change any sensor value use the "set_value" class function
        # Be aware this needs to be done AFTER the generate values function
        # Uncomment the example bellow to change the value of the temperature sensor to 16
        # ********
        # Temp_sensor.set_value(16)
        # ********

        # get the generated values
        temp = Temp_sensor.get_value()
        hum = Hum_sensor.get_value()
        co2 = CO2_sensor.get_value()
        o2 = O2_sensor.get_value()
        press = Press_sensor.get_value()

        # print values on terminal 
        print(cl.Style.BRIGHT + f"----------------------------- START SENSORS READINGS ({var}/{size}) ------------------------------")
        print(cl.Style.BRIGHT + cl.Back.YELLOW + cl.Fore.WHITE + f"Time : {t} ")
        print(cl.Fore.YELLOW + f"{names[0]} : {temp}")
        print(cl.Fore.BLUE + f"{names[1]} : {hum}")
        print(cl.Fore.MAGENTA + f"{names[2]} : {co2}")
        print(cl.Fore.CYAN + f"{names[3]} : {o2}")
        print(cl.Fore.RED + f"{names[4]} : {press}")
        print(cl.Style.BRIGHT + f"----------------------------- CTRL + C TO EXIT ------------------------------------")
        print(cl.Style.RESET_ALL)

        time.sleep(1)
        var += 1


# simulate the values for the sensors [local thread]
def simulate_function(name):
    logging.info("Thread %s: starting", name)
    # Create the sensors names
    sensors_names = ["Temp", "Hum", "CO2", "O2", "Pressure"]
    print(cl.Fore.YELLOW + "How many values to simulate? size = ",end='')
    ans = int(input())
    start_simulation(sensors_names,ans)

    logging.info("Thread %s: finishing", name)

#initializes the system [main.py] --> shows the ASCII art and identifies the execution environment  
def initialize_system():
    cl.init(autoreset=True)
    try: 
        # ASCII art
        f = open('header.txt', 'r')
        print(f.read())
        f.close()
    except:
        print_r("ERROR-[1] : Failed opening ASCII art")
    
    try:
        if os.uname()[4].startswith("arm"):
            print(cl.Back.GREEN + f"Executing on {os.uname()[4]}")
            return 1
        else:
            print_r("ERROR-[2] : Didn't found an ARM chip 'BCM***' module, please execute me in Raspberry Pi or similar...")
            return 2
    except:
            print_r("ERROR-[3] : Unable to obtain the base model of the device")

# Start the execution of the simulation file [main.py]  
def initialize_simulator():
    try:
        sim = threading.Thread(target=simulate_function, args=(1,))
        sim.start()
    except:
        print_r("ERROR-[4] : Unable to start the simulator")

# create simulated actuators
def create_actuators(names):
    Compressor = Actuator(name=names[0],min=13,max=17)
    Humidifier = Actuator(name=names[1],min=80,max=90)
    Exhauster = Actuator(name=names[2],min=10,max=80)

    # if needed add more actuators HERE:


    return Compressor, Humidifier, Exhauster

#auxiliar actuator control
def control_actuator(ac, medida, overide, modo):
    if modo == "max":
        if ((medida > ac.get_max()) or overide):
            ac.set_state(True)
        else: ac.set_state(False)
        return
        
    elif modo == "min": 
        if ((medida < ac.get_min()) or overide):
            ac.set_state(True)
        else: ac.set_state(False)
        return

#same control but with a timer
def control_actuator_timer(ac, medida, overide, modo, timer):

    if timer.checkTimer():
        if modo == "max":
            if ((medida > ac.get_max()) or overide):
                ac.set_state(True)
                timer.resetTimer()
            else: ac.set_state(False)
            return
        
        elif modo == "min": 
            if ((medida < ac.get_min()) or overide):
                ac.set_state(True)
                timer.resetTimer()
            else: ac.set_state(False)
            return


