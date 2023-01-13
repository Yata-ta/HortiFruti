import serial #for serial communication with A9     # python -m pip install pyserial
import time
import pygame #to play prerecorded message          # python -m pip install pygame
from threading import Thread

import serial.tools.list_ports as port_list
#ports = list(port_list.comports())      #Confirm open ports
#for p in ports:
#    print (p)

ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=5)

def sendcommand(command):
    AT_command = command + "\r"
    ser.write(str(AT_command).encode('ascii'))
    time.sleep(1)
    #print("sent: " + command)
    if ser.inWaiting() > 0:
        echo = ser.readline() #waste the echo
        response_byte = ser.readline()
        response_str = response_byte.decode('ascii')
        #print(response_str)
        return (response_str)
    else:
        #print("ERROR at sendcommand")
        return ("ERROR at sendcommand")

def initA9():
    if not ("OK" in (sendcommand("AT"))):
        return "ERROR at init AT"
        #print("ERROR: A9 Module not found")
    #else:
        # print("A9 Module Responding")
        # print()

    if not (("OK" in (sendcommand("AT+CMGF=1"))) and ("OK" in (sendcommand("AT+CSMP=17,167,0,0")))):  # enable txt reading
        # print("ERROR: A9 Module not online")
        return "ERROR at init online check"
    #else:
        # print("A9 Module: txt reading enabled")
        # print()

    return "OK"

def sendSMS(message, number):
    #ser.write(b'AT+CMGS="' + number.encode() + b'"\r')
    #sendcommand("AT+CMGS="+number)
    ser.write(str("AT+CMGS=" + number + "\r").encode('ascii'))
    time.sleep(0.5)
    #ser.write(message.encode() + b"\r")
    #sendcommand(message)
    ser.write(str(message).encode('ascii'))
    time.sleep(0.5)
    ser.write(bytes([26]))
    time.sleep(0.5)
    #print ("Message sent")
    time.sleep(2)
    ser.flushInput()

def playaudio(filename):
    # 800/900/1800/1900MHz
    pygame.mixer.init(frequency=44100)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    return

#checks if A9 is speaking and returns it as response
def wait_for_A9():
    echo = ser.readline()  # waste the echo
    response_byte = ser.readline()
    return response_byte.decode('ascii')

def call_aux(number,ser_aux):
    #sendcommand("ATD+" + number)
    ser.flushInput()  # clear serial data in buffer if any
    if ("OK" in (sendcommand("ATD"+number))):
        #print("possiible")
        call_status = ser.readline().decode('ascii')
        #print(call_status)
        while "+CIEV: \"CALL\",1" in call_status:
            call_status = ser.readline().decode('ascii')
            #print(call_status)
        if "+CIEV: \"SOUNDER\",0" in call_status:
            call_status = ser.readline().decode('ascii')
            #print(call_status)
            if "+CIEV: \"CALL\",0" in call_status:
                print("ME: try again later")
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
                #print("ME: declined call")
                return "DECLINED"
            if "+CIEV: \"SOUNDER\",1" in call_status:
                #print("ME: answered")
                ser.flushInput()
                playaudio("../rep/bill.mp3")
                #threading.Timer(30, sendcommand("ATH")).start()
                time.sleep(20)
                sendcommand("ATH")
                return "OK"
    return "NO REACH"

def call(number):
    thread = Thread(target=call_aux, args=(number, ser))
    thread.start()
    #thread.join()

def turn_off_serial():
    ser.close()

#"/dev/ttyUSB0"

#ser=turn_on_serial()
#initA9(ser)
#call(2,ser)

#turn_off_serial(ser)
#i=0
#while i<30:
#    time.sleep(0.5)
#    i = i+1
#    print(i)
#thread.join()
