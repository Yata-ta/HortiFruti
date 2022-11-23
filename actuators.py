import RPi.GPIO



RPi.GPIO.setmode(RPi.GPIO.BCM) # GPIO Numbers instead of board numbers

class Atuador:

    def __init__ (self, GPIO):
        self.GPIO = GPIO
        RPi.GPIO.setup(self.GPIO, RPi.GPIO.OUT) # GPIO Assign mode
        self.state = False
    
    def set_state(self, status):
        if status == True:
            #Setting State: ON
            RPi.GPIO.output(self.GPIO, RPi.GPIO.HIGH)
        elif status == False:
            #Setting State: OFF
            RPi.GPIO.output(self.GPIO, RPi.GPIO.LOW)
        else:
            #ERROR
            pass

    def toggle_state(self):
        #Setting State: ON
        if (self.state == False):
            #Setting State: ON
            RPi.GPIO.output(self.GPIO, RPi.GPIO.HIGH)
        elif (self.state == True):
            #Setting State: OFF
            RPi.GPIO.output(self.GPIO, RPi.GPIO.LOW)
        else:
            #ERROR
            pass

#########################################################
#LISTA DE ATUADORES E PINS ASSOCIADOS
#NO FINAL DESCOMENTAR
'''
PIN_VENTOINHA = 
PIN_

ATUADOR_VENTOINHA = Atuador(PIN_VENTOINHA)


'''