#include <dht.h>
dht DHT;

#define LIGHT_PIN A0
#define MOTION_1_PIN A1
#define MOTION_2_PIN A2
#define TEMP_PIN 7

void setup() {
  Serial.begin(9600);
}

void getHumidTemp() {
  int chk = DHT.read11(TEMP_PIN);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
}

void getLight() {
  int lightValue = analogRead(LIGHT_PIN);
  Serial.print("Light = ");
  Serial.println(lightValue);
}

void loop() {
  getHumidTemp();
  getLight();
  delay(5000);
}
