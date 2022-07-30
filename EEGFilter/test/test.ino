void setup() {
  Serial.begin(9600);

}

void loop() {
  int senValue=analogRead(A0);
  Serial.println(senValue);
  delay(1);
  
}
