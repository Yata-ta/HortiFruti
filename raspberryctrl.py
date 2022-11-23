# values generator for terminal
import os
import datetime as dt
import time
import colorama as cl
import socket
import pickle
import serial
import testeDB.py

actuators_names = ["Compressor", "Humidifier", "Exhauster", "O2", "Pressure"]
cl.init(autoreset=True)

class Actuator:
    def __init__(self,name,min,max):
        self.name = name
        self.state = False
        self.min = min
        self.max = max

    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

    def get_state_print(self):
        if self.state:
            return "On"
        else: return "Off"
    
    def set_state(self,state):
        self.state = state

    def get_min(self):
        return self.min
    
    def get_max(self):
        return self.max

def create_actuators(names):
    Compressor = Actuator(name=names[0],min=13,max=17)
    Humidifier = Actuator(name=names[1],min=80,max=90)
    Exhauster = Actuator(name=names[2],min=10,max=80)

    # if needed add more actuators HERE:


    return Compressor, Humidifier, Exhauster


        
class Client():
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 2021

        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
    
    def readMeasures(self):
        data = self.socket.recv(4096)
        data = data.decode('utf-8')
        return eval(data)

    def close(self):
        self.socket.close()
        
def control_actuator(ac, medida, overide, modo):
    switch (mode):
        case "max": 
            if ((medida > ac.get_max()) or overide):
                ac.set_state(True)
            else: ac.set_state(False)
            return
        
        case "min": 
            if ((medida < ac.get_min()) or overide):
                ac.set_state(True)
            else: ac.set_state(False)
            return
    

def read_oxigen():
    ser = serial.Serial('/dev/tty5',9600,8,'N',1)
    #ser.write('D')

def Main():
    
    # Create actuators for the main loop
    Comp_actuator, Hum_actuator, CO2_O2_actuator = create_actuators(actuators_names)
    client = Client()

    hum_timer = time.time()
    
    #Base de dados
    contentorId = 1
    db_con, connection = connect(DB(None, None, None, None))
    fruta, utilizadorid = identificacao(db_con, contentorId)
    tipo, valor = get_value_atuadores(db_con, contentorId)

    while (1):
        t = dt.datetime.now().strftime('%M:%S.%f')
        
        temp, hum, co2, o2, press = client.readMeasures()
        
        
        
        # Compressor Control
        control_actuator_max(Comp_actuator, temp, False)  
        
        # Humidifier Control
        # If humidifier turns On he needs to wait 1min to check Humidity again
        control_actuator_min(Hum_actuator, hum, False)

        # Exauster Control
        control_actuator_max(CO2_O2_actuator, o2, False)
        if(not CO2_O2_actuator.get_state())
            control_actuator_max(CO2_O2_actuator, co2, False)   


        
        # print values on terminal 
        print(cl.Style.BRIGHT + f"----------------------------- ACTUATOR'S STATES ------------------------------")
        print(cl.Style.BRIGHT + cl.Back.YELLOW + cl.Fore.WHITE + f"Time : {t} ")
        print(cl.Fore.YELLOW + f"{actuators_names[0]} : {Comp_actuator.get_state_print()}")
        print(cl.Fore.BLUE + f"{actuators_names[1]} : {Hum_actuator.get_state_print()}")
        print(cl.Fore.MAGENTA + f"{actuators_names[2]} : {CO2_O2_actuator.get_state_print()}")
        print(cl.Style.BRIGHT + f"----------------------------- CTRL + C TO EXIT ------------------------------------")

        # Clear terminal for better reading
        time.sleep(1)
        os.system('cls')
        # os.system('clear') #on Linux System

    client.close()
Main()
