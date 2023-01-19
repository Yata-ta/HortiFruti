/******************************************************\
    Arduino-Raspberry Pi Bidirectional Communication  
                 Created by Yatata                    
\******************************************************/


#include "Arduino.h"

#define MSG_SIZE 50
#define BAUD 9600
float AD_REF = 5;
int AD_resolution = 10;


char separator = '|';

//TODO

uint8_t oxigenio_pin = A0;



void setup() {
  
  analogReference(EXTERNAL);
  /*while (!Serial) {
    /* Wait until Connection of Serial Port
  }*/
  Serial.begin(BAUD);
 
}

void loop() {
    

    Serial.println(analogRead(A0)*5.0/1023);
  
  
}
