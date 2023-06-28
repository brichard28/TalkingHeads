int photopin= A0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int light= analogRead(photopin);
  Serial.println(light);
  delay(10);
  

}
