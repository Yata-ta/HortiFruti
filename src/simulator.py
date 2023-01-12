import multiprocessing as mp
import colorama as cl
from modules.classes import *
from modules.functions import *

names = ["Temp", "Hum", "CO2", "O2", "Pressure"]
sensor_names = ["Temperature", "Humidity", "CO2", "O2", "Pressure"]
actuators_names = ["Compressor","Humidifier","Exhaustion","Valve"]
SENTINEL = 'SENTINEL'
ON = 1
OFF = 0

def write(conn, data):
    # basic write to pipe data
    # conn - who's sending the data
    # data - buffer data being send
    conn.send(data)
    conn.send(SENTINEL)
    time.sleep(0.2)

def receive(conn):
    # Basic receive data from conn
    # conn - who's receiving data 
    time.sleep(0.2)

    return conn.recv

def generate_values(conn,names):
    # Child process that creates the sensor values
    # conn - pipe variable, in this case the child conn
    # names - sensor names 

    cl.init(autoreset=True)

    # Create sensors
    Temperature_sensor = Sensor(name=names[0],min=10,max=50)
    Humidity_sensor = Sensor(name=names[1],min=80,max=99)
    CO2_sensor = Sensor(name=names[2],min=20,max=70)
    O2_sensor = Sensor(name=names[3],min=10,max=30)
    Pressure_sensor =  Sensor(name=names[4],min=10,max=40)


    # Generate values
    t = dt.datetime.now().strftime('%M:%S.%f')
    Temperature_sensor.start_increase_value()
    Humidity_sensor.start_decrease_value()
    CO2_sensor.start_increase_value()
    O2_sensor.start_decrease_value()
    Pressure_sensor.start_decrease_value()
    
    # send initial values
    data = [t,Temperature_sensor.get_value(),Humidity_sensor.get_value(),CO2_sensor.get_value(),
                O2_sensor.get_value(),Pressure_sensor.get_value()]

    #security sleep
    #time.sleep(1)
    #send sensor data
    write(conn,data)


    for cmsg in iter(receive(conn), SENTINEL):
        print(cl.Fore.LIGHTYELLOW_EX + f"Handshake to Parent")
        write(conn,data)

        while True:
            for msg in iter(receive(conn), SENTINEL):
                #time.sleep(1)
                # loop to generate next values
                # save new values in buffer
                # send values in stream
                
                # Generate new values
                t = dt.datetime.now().strftime('%M:%S.%f')
                Temperature_sensor.increase_value()
                Humidity_sensor.decrease_value()
                CO2_sensor.increase_value()
                O2_sensor.decrease_value()
                Pressure_sensor.decrease_value()

                # child interprets
                if msg[0] == ON:
                    aux = Temperature_sensor.act_decrease_value() # make it cooler
                    Temperature_sensor.set_value(aux) # make it cooler
                    #print(f"Temp : {Temperature_sensor.get_value()}") 
                if msg[1] == ON:
                    aux = Humidity_sensor.act_increase_value() # make it cooler
                    Humidity_sensor.set_value(aux) # make it cooler
                if msg[2] == ON:
                    aux = CO2_sensor.act_decrease_value() # make it cooler
                    CO2_sensor.set_value(aux) # make it cooler
                if msg[3] == ON:
                    aux = O2_sensor.act_increase_value() # make it cooler
                    O2_sensor.set_value(aux) # make it cooler
                if msg[4] == ON:
                    aux = Pressure_sensor.act_increase_value() # make it cooler
                    Pressure_sensor.set_value(aux) # make it cooler
                
                #updates the data 
                data_updated = [t,Temperature_sensor.get_value(),Humidity_sensor.get_value(),CO2_sensor.get_value(),
                            O2_sensor.get_value(),Pressure_sensor.get_value()]

                #security sleep
                #time.sleep(1)
                #send sensor data
                write(conn,data_updated)
    




def run_sim():
    cl.init(autoreset=True)
    parent_conn, child_conn = mp.Pipe(duplex=True) # duplex pipes

    #initiate simulator
    simulator = mp.Process(target=generate_values,args=(child_conn,names))
    simulator.start()

    for msg in iter(receive(parent_conn), SENTINEL):
        # print data 
        # interpret the values
        # send act
        print(cl.Fore.LIGHTYELLOW_EX + f"Handshake to Child")
    

    #security sleep
    time.sleep(1)
    act = [OFF,OFF,OFF,OFF,OFF]
    write(parent_conn,act) # this is in loop, why???

    #loop to receive new values
    while True:
        for msg in iter(receive(parent_conn), SENTINEL):
            #print(cl.Fore.LIGHTBLUE_EX + f"Parent received : {msg}")

            #TODO database connect to obtain values margins
            # using reference ideal for now..
            temp_lim = 16.00
            hum_lim = 90.00
            CO2_lim = 50.00
            O2_lim = 25.00
            pp_lim = 30.00

            # interpret the values
            if msg[1] > temp_lim: # decrease
                act[0] = ON
            if msg[2] < hum_lim: # increase
                act[1] = ON
            if msg[3] > CO2_lim: # decrease
                act[2] = ON
            if msg[4] < O2_lim: # increase
                act[3] = ON
            if msg[5] < pp_lim: # increase
                act[4] = ON

            # print data 
            print_chamber(sensor_names,msg,actuators_names,act)
            time.sleep(1.5)
            os.system('clear')
            

            #security sleep
            #time.sleep(1)
            # send act
            write(parent_conn,act)
            act = [OFF,OFF,OFF,OFF,OFF]


