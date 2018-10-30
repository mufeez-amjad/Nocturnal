int min, max;

/*
  Connect:

  - to Ground
  + to 3.3V
  A to A0
*/



void setup() {
  Serial.begin(9600);
  min = max = analogRead(0);
}

void loop() {

  int read = analogRead(0);

  if (read < min) min = read;
  else if (read > max) max = read;

  Serial.print(read);
//  Serial.print(min);
//  Serial.print(max);
  Serial.print("\n");
  delay(200);
  
}
