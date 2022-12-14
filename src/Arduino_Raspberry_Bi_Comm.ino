/******************************************************\
    Arduino-Raspberry Pi Bidirectional Communication  
                 Created by Yatata                    
\******************************************************/

#define MSG_SIZE 50
#define BAUD 9600
float AD_REF = 5;
int AD_resolution = 10;

/* 0 Communication Arduino-Raspberry   
   1 Communication Raspberry-Arduino
   2 Communication Stand-By */
int mode = 2;

/*Format
  mode|Temp|Hum|Oxy*/
String data;
char* separator = "|";

//TODO
//uint8_t temperature_pin = A0;
//uint8_t humidity_pin = A0;
uint8_t oxigenio_pin = A0;
float temperature_value = 0.0;
float humidity_value = 0.0;
float oxigenio_value = 0.0;
int temperature_switch = 0;
int humidity_switch = 0;
int oxigenio_switch = 0;


void setup() {
  
  analogReference(EXTERNAL);
  while (!Serial) {
    /* Wait until Connection of Serial Port*/
  }
  Serial.begin(BAUD);
 
}

void loop() {

  
  if(Serial.available() > 0) {
    
    /* get Raspberry Data */
    data = Serial.readStringUntil('\n');
    Serial.print("Recebi: ");
    Serial.println(data);
    Serial.flush();
    
    mode = data.charAt(0) - '0';
    
  }else{
    mode = 2;
  }


  /* 0 Communication Arduino-Raspberry*/
  if (mode == 0){

    //get sensor data
    //oxigenio_value = analogRead(oxigenio_pin)*(AD_REF/(pow(2, AD_resolution)-1));
    temperature_value = 5.37;
    humidity_value = 88.88;
    oxigenio_value = 3.3;

    Serial.print(mode);
    Serial.print(separator);
    Serial.print(temperature_value);
    Serial.print(separator);
    Serial.print(humidity_value);
    Serial.print(separator);
    Serial.print(oxigenio_value);
    
    Serial.println();

  /* 1 Communication Raspberry-Arduino*/
  }else if (mode == 1){

      /*Format
        mode|Temp|Hum|Oxy*/
      temperature_switch = data.charAt(2) - '0';
      humidity_switch = data.charAt(4) - '0';
      oxigenio_switch = data.charAt(6) - '0';

      //TODO
      //apply Actuator Switch Relay
     
      Serial.print("Recebi Mensagem:");
      Serial.print(data);
      Serial.println();

      stringOne = "";

  }else if (mode == 2){
    
    /*Stand-By Mode*/
    
  }else{
    
    /*Error Case*/
    
  }  
}
