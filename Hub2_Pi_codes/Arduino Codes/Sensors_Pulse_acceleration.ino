// Pulse Sensor Library and Pins
  #define USE_ARDUINO_INTERRUPTS true
  #include <PulseSensorPlayground.h>
  const int OUTPUT_TYPE = SERIAL_PLOTTER;
  const int PULSE_INPUT = A0;
  const int PULSE_BLINK = 13;    // Pin 13 is the on-board LED
  const int PULSE_FADE = 5;
  const int THRESHOLD = 550;
  PulseSensorPlayground pulseSensor;
//---------------------------------------------------------------------

//---------------------------------------------------------------------
// Acceleration Sensor Library and Pins
#include <SPI.h>
#include <Adafruit_BusIO_Register.h>
#include <Adafruit_I2CDevice.h>
#include <Adafruit_I2CRegister.h>
#include <Adafruit_SPIDevice.h>
#include <Adafruit_LSM6DSOX.h>
// For SPI mode, we need a CS pin
#define LSM_CS 9
// For software-SPI mode we need SCK/MOSI/MISO pins
#define LSM_SCK 12
#define LSM_MISO 11
#define LSM_MOSI 10
Adafruit_LSM6DSOX sox;
//---------------------------------------------------------------------
// Pressure Sensor Library and Pins
#include "Wire.h"

void setup(void) {
  Serial.begin(115200);
  
  while (!Serial)
    delay(10);
  //------------------------------------------------------------------
  //Pulse sensor code
  pulseSensor.analogInput(PULSE_INPUT);
  pulseSensor.blinkOnPulse(PULSE_BLINK);
  pulseSensor.fadeOnPulse(PULSE_FADE);

  pulseSensor.setSerial(Serial);
  pulseSensor.setOutputType(OUTPUT_TYPE);
  pulseSensor.setThreshold(THRESHOLD);

  if (!pulseSensor.begin()) {
    for(;;) {
      // Flash the led to show things didn't work.
      digitalWrite(PULSE_BLINK, LOW);
      delay(50);
      digitalWrite(PULSE_BLINK, HIGH);
      delay(50);
    }
  }
  //------------------------------------------------------------------
  //Acceleration sensor code
    if (!sox.begin_I2C()) {
   //if (!sox.begin_SPI(LSM_CS)) {
   //if (!sox.begin_SPI(LSM_CS, LSM_SCK, LSM_MISO, LSM_MOSI)) {
    // Serial.println("Failed to find LSM6DSOX chip");
    while (1) {
      delay(10);
    }
  } 
//  //Serial.println("LSM6DSOX Found!");
//  // sox.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
//  //Serial.print("Accelerometer range set to: ");
//  switch (sox.getAccelRange()) {
//  case LSM6DS_ACCEL_RANGE_2_G:
//    Serial.println("+-2G");
//    break;
//  case LSM6DS_ACCEL_RANGE_4_G:
//    Serial.println("+-4G");
//    break;
//  case LSM6DS_ACCEL_RANGE_8_G:
//    Serial.println("+-8G");
//    break;
//  case LSM6DS_ACCEL_RANGE_16_G:
//    Serial.println("+-16G");
//    break;
//  } 
//  // sox.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS );
//  Serial.print("Gyro range set to: ");
//  switch (sox.getGyroRange()) {
//  case LSM6DS_GYRO_RANGE_125_DPS:
//    Serial.println("125 degrees/s");
//    break;
//  case LSM6DS_GYRO_RANGE_250_DPS:
//    Serial.println("250 degrees/s");
//    break;
//  case LSM6DS_GYRO_RANGE_500_DPS:
//    Serial.println("500 degrees/s");
//    break;
//  case LSM6DS_GYRO_RANGE_1000_DPS:
//    Serial.println("1000 degrees/s");
//    break;
//  case LSM6DS_GYRO_RANGE_2000_DPS:
//    Serial.println("2000 degrees/s");
//    break;
//  case ISM330DHCX_GYRO_RANGE_4000_DPS:
//    break; // unsupported range for the DSOX
  }
  // sox.setAccelDataRate(LSM6DS_RATE_12_5_HZ);
//  Serial.print("Accelerometer data rate set to: ");
//  switch (sox.getAccelDataRate()) {
//  case LSM6DS_RATE_SHUTDOWN:
//    Serial.println("0 Hz");
//    break;
//  case LSM6DS_RATE_12_5_HZ:
//    Serial.println("12.5 Hz");
//    break;
//  case LSM6DS_RATE_26_HZ:
//    Serial.println("26 Hz");
//    break;
//  case LSM6DS_RATE_52_HZ:
//    Serial.println("52 Hz");
//    break;
//  case LSM6DS_RATE_104_HZ:
//    Serial.println("104 Hz");
//    break;
//  case LSM6DS_RATE_208_HZ:
//    Serial.println("208 Hz");
//    break;
//  case LSM6DS_RATE_416_HZ:
//    Serial.println("416 Hz");
//    break;
//  case LSM6DS_RATE_833_HZ:
//    Serial.println("833 Hz");
//    break;
//  case LSM6DS_RATE_1_66K_HZ:
//    Serial.println("1.66 KHz");
//    break;
//  case LSM6DS_RATE_3_33K_HZ:
//    Serial.println("3.33 KHz");
//    break;
//  case LSM6DS_RATE_6_66K_HZ:
//    Serial.println("6.66 KHz");
//    break;
//  }
  // // sox.setGyroDataRate(LSM6DS_RATE_12_5_HZ);
  // Serial.print("Gyro data rate set to: ");
  // switch (sox.getGyroDataRate()) {
  // case LSM6DS_RATE_SHUTDOWN:
  //   Serial.println("0 Hz");
  //   break;
  // case LSM6DS_RATE_12_5_HZ:
  //   Serial.println("12.5 Hz");
  //   break;
  // case LSM6DS_RATE_26_HZ:
  //   Serial.println("26 Hz");
  //   break;
  // case LSM6DS_RATE_52_HZ:
  //   Serial.println("52 Hz");
  //   break;
  // case LSM6DS_RATE_104_HZ:
  //   Serial.println("104 Hz");
  //   break;
  // case LSM6DS_RATE_208_HZ:
  //   Serial.println("208 Hz");
  //   break;
  // case LSM6DS_RATE_416_HZ:
  //   Serial.println("416 Hz");
  //   break;
  // case LSM6DS_RATE_833_HZ:
  //   Serial.println("833 Hz");
  //   break;
  // case LSM6DS_RATE_1_66K_HZ:
  //   Serial.println("1.66 KHz");
  //   break;
  // case LSM6DS_RATE_3_33K_HZ:
  //   Serial.println("3.33 KHz");
  //   break;
  // case LSM6DS_RATE_6_66K_HZ:
  //   Serial.println("6.66 KHz");
  //   break;
  //}
//}

void loop(void) 
{
  delay(10);
  //Serial.println("Start of sensor data");
  

  //---------------------------------------------------------------
  //delay(30);
  // write the latest sample to Serial.
  // Serial.print("BPM");
  // Serial.print("\n");
  // pulseSensor.outputSample();

  Serial.print("Heart_rate,");
  pulseSensor.outputSample();
  
  
  //checking if the pulse sensor has detected the start of a heartbeat. 
  if (pulseSensor.sawStartOfBeat()) {
   //Serial.print("Start_Heartbeat,");
   pulseSensor.outputBeat();
   //Serial.print("\n");
  }
  //--------------------------------------------------------------
  //Acceleration Sensor 
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  sox.getEvent(&accel, &gyro, &temp);
  Serial.print("Amb_Temperature,");
  //Serial.print("\n");
  Serial.print(temp.temperature);
  Serial.print(",C,");
  //Serial.print("\n");  
  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("Accel_X,");
  //Serial.print("\n");
  Serial.print(accel.acceleration.x);
  Serial.print(",m/s^2,");
  //Serial.print("\n");
  Serial.print("Accel_Y,");
  //Serial.print("\n");
  Serial.print(accel.acceleration.y);
  Serial.print(",m/s^2,");
  //Serial.print("\n");
  Serial.print("Accel_Z,");
  //Serial.print("\n");
  Serial.print(accel.acceleration.z);
  Serial.print(",m/s^2,");
  //Serial.print("\n");
  // /* Display the results (rotation is measured in rad/s) */
  // Serial.print("Gyro X radians/s");
  // Serial.print("\n");
  // Serial.print(gyro.gyro.x);
  // Serial.print("\n");
  // Serial.print("Gyro Y radians/s ");
  // Serial.print("\n");
  // Serial.print(gyro.gyro.y);
  // Serial.print("\n");
  // Serial.print("Gyro Z radians/s ");
  // Serial.print("\n");
  // Serial.print(gyro.gyro.z);
  // Serial.print("\n");  
  //--------------------------------------------------------------


  delay(50);

  //Serial.println("End of sensor data");
  
}
