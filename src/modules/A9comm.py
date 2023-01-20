import serial #for serial communication with A9     # python -m pip install pyserial
import time
import pygame #to play prerecorded message          # python -m pip install pygame
from threading import Thread

import serial.tools.list_ports as port_list
#ports = list(port_list.comports())      #Confirm open ports
#for p in ports:
#    print (p)

ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=5)
function_return = ""
last_alarm = 0
last_alarm_sms = 0

def sendcommand(command):
    AT_command = command + "\r"
    ser.write(str(AT_command).encode('ascii'))
    #print("sent: " + command)
    while ser.inWaiting() <= 0:
        time.sleep(0.5)
        #print("\thello")
    if ser.inWaiting() > 0:
        echo = ser.readline() #waste the echo
        response_byte = ser.readline()
        response_str = response_byte.decode('ascii')
        #print(response_str)
        return (response_str)
    else:
        #print("ERROR at sendcommand")
        return ("ERROR at sendcommand")

def initA9_aux():
    global function_return
    #print("I\tinitA9_aux")
    if not ("OK" in (sendcommand("AT"))):
        function_return = "ERROR at init AT"
        return "ERROR at init AT"
        #print("ERROR: A9 Module not found")
    #else:
        # print("A9 Module Responding")
        # print()

    call_status = sendcommand("AT+RST=1")
    while not "READY" in call_status:
        if "+CREG: 3" in call_status:
            #print("no SIM inserted")
            function_return = "ERROR at SIM check"
            return "ERROR at SIM check"
        call_status = ser.readline().decode('ascii')
        #print(call_status)

    if not (("OK" in (sendcommand("AT+CMGF=1"))) and ("OK" in (sendcommand("AT+CSMP=17,167,0,0")))):  # enable txt reading
        # print("ERROR: A9 Module not online")
        function_return = "ERROR at init online check"
        return "ERROR at init online check"
    #else:
        # print("A9 Module: txt reading enabled")
        # print()
    #print("F\tinitA9_aux")
    function_return = "OK"
    return "OK"

def initA9():
    #print("I\tinitA9")
    thread2 = Thread(target=initA9_aux)
    thread2.start()
    thread2.join()
    #print("F\tinitA9")
    return function_return

def sendSMS(message, number):
    #ser.write(b'AT+CMGS="' + number.encode() + b'"\r')
    #sendcommand("AT+CMGS="+number)

    global last_alarm_sms
    time_lapse = time.time() - last_alarm_sms
    if (time_lapse >= 1*60):
        last_alarm_sms = time.time()  
        ser.write(str("AT+CMGS=" + number + "\r").encode('ascii'))
        time.sleep(0.5)
        #ser.write(message.encode() + b"\r")
        #sendcommand(message)
        ser.write(str(message).encode('ascii'))
        time.sleep(0.5)
        ser.write(bytes([26]))
        time.sleep(0.5)
        #print ("Message sent")
        #time.sleep(2)
        ser.flushInput()
    else:
        return function_return

def playaudio(filename):
    # 800/900/1800/1900MHz
    pygame.mixer.init(frequency=44100, channels=1, buffer=512, devicename=None)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    return

#checks if A9 is speaking and returns it as response
def wait_for_A9():
    # echo = ser.readline()  # waste the echo
    # response_byte = ser.readline()
    # return response_byte.decode('ascii')
    return "ok"

def call_aux(number,audio_file):
    #sendcommand("ATD+" + number)
    global function_return
    #print("I\tcall_aux")
    ser.flushInput()  # clear serial data in buffer if any
    time.sleep(0.5)
    call_status = sendcommand("ATD"+number)
    #print("call_status: ")
    #print(call_status)
    #print("fim de call_status")
    if ("OK" in call_status):
        #print("possiible")
        call_status = ser.readline().decode('ascii')
        #print(call_status)
        while ("+CIEV: \"CALL\",1" or "" or "\n") in call_status:
            call_status = ser.readline().decode('ascii')
            #print(call_status)
        if "+CIEV: \"SOUNDER\",0" in call_status:
            call_status = ser.readline().decode('ascii')
            #print(call_status)
            if "+CIEV: \"CALL\",0" in call_status:
                #print("ME: try again later")
                function_return = "BUSY"
                return "BUSY"

        if "+CIEV: \"SOUNDER\",1" in call_status:
            call_status = ser.readline().decode('ascii')
            #print(call_status)
            while not ("+CIEV: \"SOUNDER\",0" in call_status):
                call_status = ser.readline().decode('ascii')
                #print(call_status)
            call_status = ser.readline().decode('ascii')
            #print(call_status)
            if "+CIEV: \"CALL\",0" in call_status:
                print("ME: declined call")
                function_return = "DECLINED"
                return "DECLINED"
            if "+CIEV: \"SOUNDER\",1" in call_status:
                #print("ME: answered")
                ser.flushInput()
                playaudio(audio_file)
                time.sleep(20)
                sendcommand("ATH")
                #print("F\tcall_aux")
                function_return = "OK"
                return "OK"
    #print("F\tcall_aux")
    function_return = "NO REACH"
    return "NO REACH"

def call(number, audio_file):
    #print("I\tcall")
    global last_alarm
    time_lapse = time.time() - last_alarm
    if (time_lapse >= 5*60):
        thread = Thread(target=call_aux, args=(number, audio_file))
        thread.start()
        last_alarm = time.time()  
    else:
        return function_return
    #call_aux(number, audio_file)
    #i = 0
    #while i < 60:
    #    time.sleep(0.5)
    #    i = i + 1
    #    print(i)
    #print("F\tcall")
    #thread.join()
    return function_return

def turn_off_serial():
    ser.close()

