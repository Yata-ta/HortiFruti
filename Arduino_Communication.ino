void setup() {
  // put your setup code here, to run once:
  analogReference(EXTERNAL);
  Serial.begin(14400);
}

float REF = 5;
int resolution = 10;
void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(analogRead(A0)*(REF/(pow(2,resolution)-1)),2);
  delay(1);
}
