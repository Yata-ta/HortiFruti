
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

from .classes import *
from serial.tools import list_ports
from time import sleep
subprocess.run(["sudo", "pigpiod"])
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo

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
                initA9()
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
def get_OxygenValues() -> float:
    global previous
    BAUD_RATE = 9600
    TIMEOUT = 5
    PORT = "/dev/ttyACM0"
    #PORT = "/dev/ttyAMA0"
    SEPERATOR = "|"
    
    value = 0.0
        
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    #print(myports)
    ser = serial.Serial(PORT, BAUD_RATE, timeout = TIMEOUT) # Open the serial port
    

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

    if (value >= 23 or value <= 15):
        
        if (previous <= 23 or previous >= 15):
            value = previous
        else:
            value = 3.9*19/3.80

    elif (value <= 23 and value >= 15):
        value = value
    else:
        value = 0.0
        
    return value


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

        else:
            print("INVALID argument to main.py! please choose one of the following...")
            print("DEBUG - for debug process (this mode will protect the database from flooding)")
            print("NORMAL - for normal program execution")
            print("EXAMPLE - $ sudo python3 main.py DEBUG")
            return 2

    except:
            print("MISSING argument to main.py! please choose one of the following...")
            print("DEBUG - for debug process (this mode will protect the database from flooding)")
            print("NORMAL - for normal program execution")
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
    try:
        if (real_values[0] >= limits_values[0]):
            ## Make the room colder --> turn on frizzer
            relay_module.turn_on_relay_2()
                
        if (real_values[0] <= limits_values[0]):
            ## temperature too low --> turn off frizzer
            relay_module.turn_off_relay_2()
    except:
        pass

def actuate_servo():
    print(cl.Style.RESET_ALL)
    try:
        print(f"servo value: {servo.value}")
        if servo.value == -0.0: # servo on closed position
            servo.max() # open servo
            print(f"servo value max: {servo.value}")

        elif servo.value == 1.0: # servo is open 
            servo.mid() # close servo
            print(f"servo value mid: {servo.value}")
        
        else:
            print(cl.Back.RED + "[ERROR - 7] - Invalid servo position")

    except:
        print(cl.Back.RED + "[ERROR - 6] - Error turning futaba servo")
        print(cl.Style.RESET_ALL)

def initial_components_test():
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

def log_data(data):
    log = open("../rep/log.txt",'a')
    time_date = strftime("%H:%M:%S", gmtime())
    log.write(f"{time_date}; {data[0]}; {data[1]};\n")
    log.close()
