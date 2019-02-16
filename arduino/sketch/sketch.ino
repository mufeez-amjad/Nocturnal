#include <dht.h>
dht DHT;

#include <Wire.h>
#define MPU_ADDRESS 0x68

#define LIGHT_PIN A0
#define TEMP_PIN 7

#define TIME 2000

double absolute(double x) {
  return x < 0 ? -x : x;
}

void setup() {
  Wire.begin();
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // wakes up MPU6050
  Wire.endTransmission(true);
  Serial.begin(9600);
}

void getHumidTemp() {
  int chk = DHT.read11(TEMP_PIN);
  Serial.print("Temperature:");
  Serial.println(DHT.temperature);
  Serial.print("Humidity:");
  Serial.println(DHT.humidity);
}

void getLight() {
  int lightValue = analogRead(LIGHT_PIN);
  Serial.print("Light:");
  Serial.println(lightValue);
}

double max_activity = 0;

void calcMotion() {
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x3B); //starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDRESS,14,true); // request a total of 14 registers
  int accelX = Wire.read() << 8|Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  int accelY = Wire.read()<<8|Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  int accelZ = Wire.read()<<8|Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  int temp = Wire.read()<<8|Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  int gyroX = Wire.read()<<8|Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  int gyroY = Wire.read()<<8|Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  int gyroZ = Wire.read()<<8|Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  if (accelX > 25100) accelX = 25100;
  else if (accelX < 9100) accelX = 9100;
  if (gyroZ > 3300) gyroZ = 3300;
  else if (gyroZ < -3700) gyroZ = -3700;
  if (gyroY > 3500) gyroY = 3500;
  else if (gyroY < -3500) gyroY = -3500;
  
  double activity = ((double(absolute(accelX - 17100)) / 8000) + (double(absolute(gyroZ + 200)) / 3500) + (double(absolute(gyroY)) / 3500)) / 3;
  if (activity > max_activity) max_activity = activity;
}

void getMotion() {
  Serial.print("Activity:");
  Serial.println(max_activity);
}

int ms = 0;

void loop() {
  if (ms == 100) {
    getHumidTemp();
    getLight();
    getMotion();
    Serial.println("END");
    max_activity = 0;
    ms = 0;
  }
  calcMotion();
  ms++;
  delay(10);
}
