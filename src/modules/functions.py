
## *************************************** ##
        ## Function Repository file ##
## *************************************** ##
## ** Created by Gabriel Pizzighini and ... ** ## 

import os
import subprocess
import colorama as cl
import platform
import logging
import threading
import atexit
import time
import serial
import RPi.GPIO as GPIO
import board
import adafruit_bme680
import adafruit_ens160
import smbus
from .database import *
from .A9comm import *
from .db_control import *

from .classes import *
from serial.tools import list_ports
from time import sleep
subprocess.run(["sudo", "pigpiod"])
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import modules.db_control

import time
import pandas as pd

factory = PiGPIOFactory()
servo = Servo(23, pin_factory=factory)

# prints error [local]
def print_r(str):
    print(cl.Back.RED + str)
    print(cl.Style.RESET_ALL)

# prints in yellow [local]
def print_y(str):
    print(cl.Fore.YELLOW + str)
    print(cl.Style.RESET_ALL)

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
        f = open('../rep/header.txt', 'r')
        print(f.read())
        f.close()
    except:
        print_r("ERROR-[1] : Failed opening ASCII art")
    
    try:
        if platform.uname()[4].startswith("aarch64"):
            print(cl.Back.GREEN + f"Executing on {platform.uname()[4]}")
            ## Set relays pins mode to default 
            relay_module = Relay(1)
            relay_module.deafult_state()

            try:
                if os.path.exists("../rep/log.txt"):
                    os.remove("../rep/log.txt")

                # start A9 comm
                #initA9()
                print_r("entrou")
                return 1
            except:
                print_r("ERROR-[9] : Unable to delete old log file")
        else:
            print_r("ERROR-[2] : Didn't found an ARM chip 'BCM***' module, please execute me in Raspberry Pi or similar...")
            print(cl.Back.RED + f"You are on a {platform.system()} system")
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

def initialize_real_sensors():
    """
    Check if all sensors are connected
    @param\n
    Location - defines the geographical location of the raspberry, supported locations = [PT] & [BR]
    """
    i2c = board.I2C()  # uses board.SCL and board.SDA

    try:
        global bme680 
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
        print("[" + cl.Fore.GREEN + "OK" + cl.Fore.WHITE + "]" + "- BME680 connected")

    except:
        print("[" + cl.Fore.RED + "NOT FOUND" + cl.Fore.WHITE + "]" + "- BME680 not found")
        pass

    try:
        global ens160
        ens160 = adafruit_ens160.ENS160(i2c)
        print("[" + cl.Fore.GREEN + "OK" + cl.Fore.WHITE + "]" + "- ENS160 connected")

    except:
        print("[" + cl.Fore.RED + "NOT FOUND" + cl.Fore.WHITE + "]" + "- ENS160 not found")  
        pass


#global previous
previous = 3.9*19/3.80
def UART(ser):
    global previous
    while True:
        try:
            msg_recebida = ser.readline().strip().decode("utf-8")
                
                #ser.flush()
            break
      
        except UnicodeDecodeError:
                #print(".",end="")
            msg_recebida = ser.readline().strip().decode("utf-8")
        
                #ser.flush()
            pass  
        
    try:
        value = float(msg_recebida)*19/3.80
        previous = value
    except ValueError:
        value = previous
    
    return value


def get_OxygenValues() -> float:
    global previous
    BAUD_RATE = 9600
    TIMEOUT = 5
    PORT = "/dev/ttyACM0"
    #PORT = "/dev/ttyAMA0"
    SEPERATOR = "|"
    previous = 0
    value = 0.0
        
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    #print(myports)
    ser = serial.Serial(PORT, BAUD_RATE, timeout = TIMEOUT) # Open the serial port
    
    value = UART(ser)
    
    while(value > 0):

        if (value >= 25 or value <= 15):
        
            if (previous < 23 and previous > 15):
                value = previous
            else:
                value = UART(ser)
        else:  
            return round (value,2)
    return 0.0

def read_real_sensors(Location: str):
    """
    Read data from the sensors\n
    @param\n
    Location - defines the geographical location of the raspberry, supported locations = [PT] & [BR]
    @return\n
    [0] - Temperature in celsius\n
    [1] - Gas\n
    [2] - Humidity\n
    [3] - Pressure in hPa\n
    [4] - eC02 in ppm\n
    """

    try:
        # Calibration of pressure 
        if Location == "PT":
            # change this to match the location's pressure (hPa) at sea level
            bme680.sea_level_pressure = 1008.5

        elif Location == "BR":
            # change this to match the location's pressure (hPa) at sea level
            bme680.sea_level_pressure = 1012.5
        else: 
            print_r(f"ERROR-[4] : Location '{Location}' not found or invalid")

        # temperature calibration
        temperature_offset = -5

        # Set the temperature compensation variable to the ambient temp
        # for best sensor calibration
        #ens160.temperature_compensation = bme680.temperature + temperature_offset
        ens160.temperature_compensation = bme680.temperature + temperature_offset

        # Same for ambient relative humidity
        # ens160.humidity_compensation = bme680.humidity
        ens160.humidity_compensation = bme680.relative_humidity

        return bme680.temperature + temperature_offset, bme680.gas, bme680.relative_humidity, bme680.pressure, ens160.eCO2
        
    except:
        print_r(f"ERROR-[5] : Unable to start real sensors ")

def start(argv)->int:
    '''
    Mode function to protect the database 
    '''
    try:
        if argv[1] == 'DEBUG':
            print("Entering" + cl.Fore.LIGHTYELLOW_EX + " DEBUG " + cl.Fore.WHITE + "mode to protect from database flood")
            return 0

        elif argv[1] == 'NORMAL':
            print("Entering" + cl.Fore.LIGHTGREEN_EX + " NORMAL " + cl.Fore.WHITE + "mode")
            return 1
        
        elif argv[1] == 'TEST':
            print("Entering" + cl.Fore.LIGHTGREEN_EX + " TEST " + cl.Fore.WHITE + "mode")
            return 3

        else:
            print("INVALID argument to main.py! please choose one of the following...")
            print("DEBUG - for debug process (this mode will protect the database from flooding)")
            print("NORMAL - for normal program execution")
            print("TEST - for a connected component test")
            print("EXAMPLE - $ sudo python3 main.py DEBUG")
            return 2

    except:
            print("MISSING argument to main.py! please choose one of the following...")
            print("DEBUG - for debug process (this mode will protect the database from flooding)")
            print("NORMAL - for normal program execution")
            print("TEST - for a connected component test")
            print("EXAMPLE - $ sudo python3 main.py DEBUG") 

def alarm(pin, mode = "off"):
    '''
    Turns on and off the alarm led (red led) #
    set the correct pin on the GPIO, remember is BCM!
    mode = on --> led on
    mode = off --> led off 
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    if mode == "on":
        GPIO.output(pin, True)
    else:
        GPIO.output(pin, False)

@atexit.register
def termination_handler():
    print(cl.Fore.LIGHTRED_EX +"Exiting program", end='')
    # set all pins back to default 
    relay_module = Relay(1)
    relay_module.deafult_state()
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    time.sleep(0.5)
    print(cl.Fore.LIGHTRED_EX +".", end="")
    turn_off_serial()
    time.sleep(0.5)
    print(cl.Fore.LIGHTRED_EX +".", end="")
    time.sleep(0.5)
    print(cl.Fore.LIGHTRED_EX +".", end="")
    time.sleep(0.5)
    print(cl.Fore.LIGHTRED_EX +"Done")
    print(cl.Style.RESET_ALL)

def atuator_logic(room: int, relay_module, real_values: list, limits_values: list):
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
    try:
        #Temperature control
        if (real_values[0] >= limits_values[0]):
            ## Make the room colder --> turn on frizzer
            relay_module.turn_on_relay_1()
                
        if (real_values[0] <= limits_values[1]):
            ## Make the room hotter --> turn off frizzer
            relay_module.turn_off_relay_1()
    except:
        print_r(f"ERROR-[10] : Malfunction on relay 1 ")
    
    try:
        #Humidity control
        if (real_values[2] >= limits_values[2]):
            ## Make the room steamer --> turn on humidifier
            relay_module.turn_on_relay_3()
                
        if (real_values[2] <= limits_values[3]):
            ## Make the room dryier --> turn off humidifier
            relay_module.turn_off_relay_3()
    except:
        print_r(f"ERROR-[11] : Malfunction on relay 2")
    
    try:
        #O2 and CO2 control
        if (real_values[1] >= limits_values[4] or real_values[4] >= limits_values[6] ):
            ## Make the room oxigenize --> turn on exaustion
            relay_module.turn_on_relay_2()
                
        if (real_values[1] <= limits_values[5] or real_values[4] <= limits_values[7]):
            ## Make the room isolate --> turn off exaustion
            relay_module.turn_off_relay_2()
    except:
        print_r(f"ERROR-[12] : Malfunction on relay 3")
    
    try:
        # CAUTION --> We cannot open the valves when the door is open!
        #Pessure control
        if (real_values[3] >= limits_values[8]):
            ## Remove gases --> open door
            actuate_servo()
                
        if (real_values[3] <= limits_values[9]):
            if (actuate_servo() == True):
                # check if the door is open and
                actuate_servo() # --> closes and
            ## Insert Gases --> turn on cilinder valves
            relay_module.turn_on_relay_4()
    except:
        print_r(f"ERROR-[13] : Malfunction on relay 3 or 4")

def actuate_servo():
    '''
    Opens and closes the servo based on its previous position\n
    @returns\n
    True if its now open\n
    False if its now closed\n 
    '''
    print(cl.Style.RESET_ALL)
    try:
        print(f"servo value: {servo.value}")
        if servo.value == -0.0: # servo on closed position
            servo.max() # open servo
            print(f"servo value max: {servo.value}")
            return True # True --> for open position 

        elif servo.value == 1.0: # servo is open 
            servo.mid() # close servo
            print(f"servo value mid: {servo.value}")
            return False # False --> for close position 
        
        else:
            print(cl.Back.RED + "ERROR-[7] : Invalid servo position")

    except:
        print(cl.Back.RED + "ERROR-[6] : Error turning futaba servo")
        print(cl.Style.RESET_ALL)

def initial_components_test(call_number):
    '''
    EXECUTE OUT OF THE MAIN LOOP
    This function tests the actuation of the circut components
    -> futaba servo : open--2s--close--2s
    -> relays : x--on--1s--of--1s [x = relay number]
    -> Alarm : on--0.5s--0ff--0.5s--on--0.5s--off 
    '''

    print("****SERVO TEST****")
    actuate_servo()
    sleep(1)
    actuate_servo()
    sleep(1)
    print("***DONE!***")
    print()
    print("****RELAY TEST****")
    relay_module = Relay(1)

    relay_module.turn_on_relay_1()
    sleep(1)
    relay_module.turn_off_relay_1()

    relay_module.turn_on_relay_2()
    sleep(1)
    relay_module.turn_off_relay_2()

    relay_module.turn_on_relay_3()
    sleep(1)
    relay_module.turn_off_relay_3()
    
    relay_module.turn_on_relay_4()
    sleep(1)
    relay_module.turn_off_relay_4()
    print("***DONE!***")
    print()

    alarm_pin = 25 ## red
    print(f"****ALARM TEST on pin {alarm_pin}****")
    alarm(alarm_pin,"on")
    sleep(0.5)
    alarm(alarm_pin,"off")
    sleep(0.5)
    alarm(alarm_pin,"on")
    sleep(0.5)
    alarm(alarm_pin,"off")
    print("***DONE!***")
    print()

    print("*** START A9 COMMUNICATION ? ***")
    res = input("(yes/no): ")
    if res.lower() == 'yes':
        print(f"*** STARTING CALL ON NUMBER: {call_number} ***")
        call(call_number)
        print("***DONE!***")
        print(f"*** SEND SMS to number: {call_number}")
        print("....IN WORK....")
        print("***DONE!***")
    else:
        exit()




def log_data(sensor_data,actuator_data):
    '''
    function to create logs after the offline signal\n
    @inputs\n
    sensor_data => [real-temp-value,real-hum-value,real-O2-value,real-CO2-value,real-Press-value]\n
    actuator_data => [K1,K3,K5,K7] -> k is equal to the relay on the relay module ex:[1,2,3,4]
    '''
    log = open("../rep/log.txt",'a')
    time_date = strftime("%H:%M:%S", gmtime())
    log.write(f"{time_date}; {sensor_data[0]}; {sensor_data[1]}; {sensor_data[2]}; {sensor_data[3]}; {sensor_data[4]}; {actuator_data[0]}; {actuator_data[1]}; {actuator_data[2]}; {actuator_data[3]}\n")
    log.close()

def check_internet(hostname,last_value,db_connected):
    """
    checks for internet connection by reaching the DNS 1.1.1.1 on the server
    """
    global Connection_SIGNAL
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        if last_value == "OFFLINE":
            ## switch from offline to online now we send the log to the database
            print("Starting process_and_send function on a thread")
            # OFFLINE to ONLINE --> there is a new log
            # we are back online! lets create and send the logged information back to the db in a thread
            thread = Thread(target=process_and_send(db_connected))
            thread.start()
            Connection_SIGNAL = "ONLINE"
        return True, Connection_SIGNAL
    except Exception:
        print("[" + cl.Fore.RED + "ERROR" + cl.Fore.WHITE + "]" + "- Lost internet connection")
        if last_value == "ONLINE":
            #lost connection to the database now we must log data
            Connection_SIGNAL = "OFFLINE"
        pass # we ignore any errors, returning False
        return False, Connection_SIGNAL


def get_sensors(sensors,COUNTRY):  #do arduino

    temp, gas, humidade, pressao, co2 = modules.functions.read_real_sensors(COUNTRY)  
    for sensor in sensors:
        if(sensor.name =="temperatura"):
            sensor.value = temp
            print('The new value from sensor ', sensor.name,' is ', sensor.value)
        elif (sensor.name =="CO2"):
            sensor.value = co2
            print('The new value from sensor ', sensor.name,' is ', sensor.value)
        elif (sensor.name =="O2"):
            sensor.value = get_OxygenValues()
            print('The new value from sensor ', sensor.name,' is ', sensor.value)
        elif (sensor.name =="humidade"):
            sensor.value = humidade
            print('The new value from sensor ', sensor.name,' is ', sensor.value)
        elif (sensor.name =="pressao"):
            sensor.value = pressao
            print('The new value from sensor ', sensor.name,' is ', sensor.value)
    return  sensors

def send_db_sensor_buffer(db_connected):
    if db_connected is True:
        data_df = pd.read_csv('sensor_data.csv')

        range_for = min(20, data_df.shape[0])

        for i in range(range_for):

            print(i)

            id = data_df.iloc[0]['id']
            time = data_df.iloc[0]['Time']
            value = data_df.iloc[0]['Value']
            modules.db_control.set_value_sensor(id, time, value)

            print(id, time, value)

            data_df.drop(data_df.index[0], axis=0, inplace=True)

        data_df.to_csv('sensor_data.csv', index=False)

    return

def send_db_actuator_buffer(db_connected):
    if db_connected is True:
        data_df = pd.read_csv('actuator_data.csv')

        range_for = min(20, data_df.shape[0])

        for i in range(range_for):

            print(i)

            id = data_df.iloc[0]['id']
            time = data_df.iloc[0]['Time']
            value = data_df.iloc[0]['Value']
            modules.db_control.set_value_atuador(id, time, value)

            print(id, time, value)

            data_df.drop(data_df.index[0], axis=0, inplace=True)

        data_df.to_csv('actuator_data.csv', index=False)

    return

def define_sensors(contentorId,db_connected):
    sensors = []
    data_df = []
    
    if db_connected is True:
   
        # Open db connection
        sensors_db = modules.db_control.get_value_sensores(contentorId)
   
        for i in range(len(sensors_db)):
            sensor_aux = modules.classes.Sensor(-1, contentorId, 'ini', 0, 0)

            sensor_aux.id = sensors_db[i][0]
            sensor_aux.name = sensors_db[i][1]
            sensor_aux.value = sensors_db[i][2]
            sensor_aux.max = sensors_db[i][4]
            sensor_aux.min = sensors_db[i][5]

            sensors.append(sensor_aux)
      

            data_df.append([sensor_aux.name, sensor_aux.id, sensor_aux.value, sensor_aux.min, sensor_aux.max])
  
        df_sensors = pd.DataFrame(data_df, columns=['Type','id','Current_Value','Min','Max'])
        df_sensors.to_csv("sensors.csv")

        return sensors

    else:
        df_sensors = pd.read_csv('sensors.csv')

        for i in range(df_sensors.shape[0]):
            sensor_aux = modules.classes.Sensor(-1, contentorId, 'ini', 0, 0)

            sensor_aux.name = df_sensors.iloc[i]['Type']
            sensor_aux.value = df_sensors.iloc[i]['Current_Value']
            sensor_aux.min = df_sensors.iloc[i]['Min']
            sensor_aux.max = df_sensors.iloc[i]['Max']
            sensor_aux.id = df_sensors.iloc[i]['id']

            sensors.append(sensor_aux)

        return sensors

    # Add the sensor values to the db and also to the buffer (local memory)
def set_sensors(sensors, time_day,temp_sens_passado,db_connected,timing_sens):
  
  if(timing_sens < time.time() - temp_sens_passado): 

    if db_connected is True:

        for sensor in sensors:
            modules.db_control.set_value_sensor(sensor.id, time_day, sensor.value)
        temp_sens_passado = time.time()
        

    # buffer part
    else:
        df_data = pd.read_csv('sensor_data.csv')

        for sensor in sensors:
            row = [sensor.id, time_day, sensor.value]
            df_data.loc[len(df_data)] = row

        df_data.to_csv('sensor_data.csv', index=False)
        temp_sens_passado = time.time()
        

    print("--- Mandou Para a DB ---") 

  return temp_sens_passado



def atualiza_sensores(contentorId, sensors, time, temp_sens_passado,COUNTRY,db_connected,timing_sens):
    try:
        sensors = define_sensors(contentorId)
    except:
        print('Could not connect with the db')

    sensors = get_sensors(sensors,COUNTRY)

    #try:
    temp_sens_passado = set_sensors(sensors, time,temp_sens_passado,db_connected,timing_sens)
    #except:
    #    print('Could not connect with the db')

    return temp_sens_passado, sensors

def define_actuators(contentorId,db_connected):
    actuators = []
    data_df = []

    if db_connected is True:

        # Open db connection
        actuators_db = modules.db_control.get_value_atuadores(contentorId)

        for i in range(len(actuators_db)):
            actuator_aux = modules.classes.Actuator(-1, contentorId, 'ini', 0, 0)

            actuator_aux.id = actuators_db[i][0]
            actuator_aux.name = actuators_db[i][1]
            actuator_aux.value = actuators_db[i][2]
            actuator_aux.dashboard = actuators_db[i][4]
            actuator_aux.time_passed = 0
            actuators.append(actuator_aux)
            data_df.append([actuator_aux.name, actuator_aux.id, actuator_aux.value, actuator_aux.dashboard])

        df_actuators = pd.DataFrame(data_df, columns=['Type','id','Current_Value','dashboard'])
        df_actuators.to_csv("actuators.csv")

        return actuators

    else:
        df_actuators = pd.read_csv('actuators.csv')

        for i in range(df_actuators.shape[0]):
            actuator_aux = modules.classes.Actuator(-1, contentorId, 'ini', 0, 0)

            actuator_aux.name = df_actuators.iloc[i]['Type']
            actuator_aux.value = df_actuators.iloc[i]['Current_Value']
            actuator_aux.id = df_actuators.iloc[i]['id']
            actuator_aux.dashboard = df_actuators[i]['dashboard']
            actuator_aux.time_passed = 0
            actuators.append(actuator_aux)

        return actuators





def control_atuatores(sensores, atuadores,contentorid,time,timing_actu,relay_module,dbconnect): # todos


    for atuador in atuadores:
        
        if(atuador.name == "Frigorifico"):
                nivel = 0
                if dbconnect == True:
                    nivel = modules.db_control.get_nivel(atuador.id)
                control_frigorifico(sensores,nivel,atuador,time,timing_actu,relay_module,dbconnect)
                
        if(atuador.name == "Ventoinha"):
                nivel = 0
                if dbconnect == True:
                    nivel = modules.db_control.get_nivel(atuador.id)                
                    control_ventoinha(sensores,nivel,atuador,time,timing_actu,relay_module,dbconnect)
    for atuador in atuadores:      
             
        if(atuador.name == "Porta"):
                nivel = 0
                if dbconnect == True:
                    nivel = modules.db_control.get_nivel(atuador.id)                
                control_porta(sensores,nivel,atuador,contentorid,time,timing_actu,relay_module,dbconnect)

    return

def get_temperatura_info(sensores):
    #print("get_temp_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "temperatura"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
        
    return None, None, None

def get_CO2_info(sensores):
    #print("get_CO2_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "CO2"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
       
    return None, None, None

def get_O2_info(sensores):
    #print("get_O2_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "O2"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
        
    return None, None, None

def get_humidade_info(sensores):
    #print("get_HUM_info")
    for sens_indiv in sensores:
        if(sens_indiv.name == "humidade"):
            return sens_indiv.value, sens_indiv.max, sens_indiv.min
        
    return None, None, None

def add_actuator_data_buffer(value, actuator, time):

    df_data = pd.read_csv('actuator_data.csv')

    row = [actuator.id, time, value]
    df_data.loc[len(df_data)] = row

    df_data.to_csv('actuator_data.csv', index=False)
    return

def muda_frigorifico(valor, atuador, time,db_connected,relay_module):
    # get_specific_value_atuador
    # manda comando pro arduino
    
    try:  
        if(valor == 1):
            relay_module.turn_on_relay_1()
        elif (valor == 0):
            relay_module.turn_off_relay_1()
    except:
        print(f"ERROR-[10] : Malfunction on relay 1 ")

    if db_connected is True:
        modules.db_control.set_value_atuador(atuador.id, time, valor)

    else:
        add_actuator_data_buffer(valor, atuador, time)
    atuador.state = valor
    print(atuador.name, "mudou para ", valor)
    return


def muda_ventoinha(valor, atuador, time,db_connected,relay_module):
    # manda comando pro arduino
    try:  
        if(valor == 1):
            relay_module.turn_on_relay_2()
        elif (valor == 0):
            relay_module.turn_off_relay_2()
    except:
        print(f"ERROR-[10] : Malfunction on relay 1 ")


    if db_connected is True:
        modules.db_control.set_value_atuador(atuador.id, time, valor)
    else:
        add_actuator_data_buffer(valor, atuador, time)
    atuador.state = valor
    print(atuador.name, "mudou para ", valor)
    return


def muda_porta(valor, atuador, time,db_connected,relay_module):
    # manda comando pro arduino
    try:
        print(valor , atuador.state)
        if(valor == 1 and atuador.state!=1):
            modules.functions.actuate_servo()
        elif (valor == 0 and atuador.state!=0):
            if (modules.functions.actuate_servo() == True):
                # check if the door is open and
                modules.functions.actuate_servo() # --> closes and
            ## Insert Gases --> turn on cilinder valves
            relay_module.turn_on_relay_4()
    except:
        print(f"ERROR-[10] : Malfunction on relay 1 ")

    
    if db_connected is True:
        modules.db_control.set_value_atuador(atuador.id, time, valor)
    else:
        add_actuator_data_buffer(valor, atuador, time)
    atuador.state = valor
    print(atuador.name, "mudou para ", valor)
    return

def control_frigorifico(sensores, nivel, atuador,time_day,timing_actu,relay_module,db_connected):
    
    temp, max_, min = get_temperatura_info(sensores)
    if(nivel == 0):         # quem manda é a raspberry
      if(timing_actu < time.time() - atuador.time_passed): 
        if(temp > max_):
            muda_frigorifico(1,atuador,time_day,db_connected,relay_module)
            atuador.time_passed = time.time()
        elif(temp < min):
            muda_frigorifico(0,atuador,time_day,db_connected,relay_module)
            atuador.time_passed = time.time()
    elif(nivel != 0):
        muda_frigorifico(max(nivel,0),atuador,time_day,db_connected,relay_module)

    return

def control_ventoinha(sensores, nivel, atuador,time_day,timing_actu,relay_module,db_connected):
    CO2, max_1, min_1 = get_CO2_info(sensores)
    O2, max_2, min_2 = get_O2_info(sensores)

    if(nivel == 0):         # quem manda é a raspberry
      if(timing_actu < time.time() - atuador.time_passed): 

        if(CO2 > max_1 or O2 > max_2):               # falta aqui hierarquia. quem manda?? CO2, O2, o minimo ou o maximo??
            muda_ventoinha(1,atuador,time_day,db_connected,relay_module)
            atuador.time_passed = time.time()

        elif(CO2 < min_1 or O2 < min_2):
            muda_ventoinha(0,atuador,time_day,db_connected,relay_module)
            atuador.time_passed = time.time()

    elif(nivel != 0):
        muda_ventoinha(max(nivel,0),atuador,time_day,db_connected,relay_module)
    
    return

def control_porta(sensores, nivel, atuador, contentorid,time_day,timing_actu,relay_module,db_connected):
    ventoinha = modules.db_control.get_specific_value_atuador(str(contentorid), "Ventoinha",None)
    hum, max_, min = get_humidade_info(sensores)
    if(nivel == 0):         # quem manda é a raspberry
      if(timing_actu < time.time() - atuador.time_passed): 
        if(hum > max_ or ventoinha == 1):
            muda_porta(1,atuador,time_day,db_connected,relay_module)
            atuador.time_passed = time.time()
        elif(hum < min and ventoinha == 0):
            muda_porta(0,atuador,time_day,db_connected,relay_module)
            atuador.time_passed = time.time()
    elif(nivel != 0):
        muda_porta(max(nivel,0),atuador,time_day,db_connected,relay_module)

    return


def verifica_contentor( raspberry_id):
    
    PATH = './contentores_id.txt'
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        f = open('contentores_id', 'r')
        id = []
        for line in f:
            id.append(line)
        f.close()
        
        return id
    else:
         f = open('contentores_id', 'w')
         ids = modules.db_control.get_id_contentores(raspberry_id)
         f.writelines(str(ids))
         f.close()
         
         return ids


def process_and_send(db_connected):
        send_db_sensor_buffer(db_connected)
        send_db_actuator_buffer(db_connected)
