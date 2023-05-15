//Pinout:
//pulse sensor = A0
//water sensor = A1
// Battery = A2
//pressure sensor = A3
//Temp sensor = D4
//Acceleration sensor = A4 A5

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
//Body temperature sensor Library and Pins
 #include <OneWire.h>
#include <DallasTemperature.h>
// Data wire is conntec to the Arduino digital pin 4
#define ONE_WIRE_BUS 4
// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);
//---------------------------------------------------------------------
// Liquid sensor Library and Pins
// Configuration values:
  #define SERIES_RESISTOR     560    // Value of the series resistor in ohms.    
  #define SENSOR_PIN          A1      // Analog pin which is connected to the sensor. 

 //#define ZERO_VOLUME_RESISTANCE   4000  // Resistance value (in ohms) when no liquid is present.
  //#define CALIBRATION_RESISTANCE   2500      // Resistance value (in ohms) when liquid is at max line.
  //define CALIBRATION_VOLUME       650       // Volume (in any units) when liquid is at max line.
  #define ZERO_VOLUME_RESISTANCE   2400   // Resistance value (in ohms) when no liquid is present.
  #define CALIBRATION_RESISTANCE   410      // Resistance value (in ohms) when liquid is at max line.
  #define CALIBRATION_VOLUME       650       // Volume (in any units) when liquid is at max line.

  const int maxWaterLevel = 650; // Maximum water level in mm
  const int sensorMax = 650; // Sensor value when the eTape is submerged in water
  const int sensorMin = 2400; // Sensor value when there is no liquid 
  float waterLevel = 0;
  float waterPercent = 0;
//---------------------------------------------------------------------

//---------------------------------------------------------------------
// Pressure Sensor Library and Pins
#include "Wire.h" //allows communication over i2c devices
//#include "LiquidCrystal_I2C.h" //allows interfacing with LCD screens

const int pressureInput = A3; //select the analog input pin for the pressure transducer
const int pressureZero = 102.4; //analog reading of pressure transducer at 0psi
const int pressureMax = 921.6; //analog reading of pressure transducer at 100psi
const int pressuretransducermaxPSI = 150; //psi value of transducer being used
const int sensorreadDelay = 250; //delay in ms, constant integer to set the sensor read delay in milliseconds

float pressureValue = 0; //variable to store the value coming from the pressure transducer
float pressurePercent = 0;
//LiquidCrystal_I2C lcd(0x3f, 20, 4); //sets the LCD I2C communication address; format(address, columns, rows)

//---------------------------------------------------------------------
// Battery gauge Pins
int battery_pin = A2;

//---------------------------------------------------------------------

void setup(void) { 
  Serial.begin(115200);

  analogReference(DEFAULT); //set reference voltage to internal
  
  while (!Serial)
    delay(10);
  //------------------------------------------------------------------
  //Body temp Sensor 
  sensors.begin();
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
  //Serial.print("Start of sensor data for Hub 1,");

  //------------------------------------------------------------------
  //Pressure sensor Code
  pressureValue = analogRead(pressureInput); //reads value from input pin and assigns to variable
  pressureValue = ((pressureValue-pressureZero)*pressuretransducermaxPSI)/(pressureMax-pressureZero); //conversion equation to convert analog reading to psi
  Serial.print(",Pressure,"); // psi
  Serial.print(pressureValue, 1); //prints value from previous line to serial
  pressurePercent = (pressureValue / (pressuretransducermaxPSI-19.6))*100; //max 130psi , rated 150psi but it stops at 130pso
  Serial.print(",P_Capacity_%,");
  Serial.print(pressurePercent); // %
  //Serial.print("\n");
  //lcd.setCursor(0,0); //sets cursor to column 0, row 0
  //lcd.print("Pressure:"); //prints label
  //lcd.print(pressureValue, 1); //prints pressure value to lcd screen, 1 digit on float
  //lcd.print("psi"); //prints label after value
  //lcd.print("   "); //to clear the display after large values or negatives
  //Serial.print("\n");
  delay(20);
  //------------------------------------------------------------------
  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 
  
  Serial.print(",Body_temp_C,");
  // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  Serial.print(sensors.getTempCByIndex(0)); 
  Serial.print(",Body_temp_F,");
  Serial.print(sensors.getTempFByIndex(0));
  //delay(50);
  //---------------------------------------------------------------
  //delay(30);
  // write the latest sample to Serial.
  // Serial.print("BPM");
  // Serial.print("\n");
  // pulseSensor.outputSample();
  
  Serial.print(",Heart_rate,");
  pulseSensor.outputSample();
  //Serial.println("\n");
  //checking if the pulse sensor has detected the start of a heartbeat. 
  if (pulseSensor.sawStartOfBeat()) {
   //Serial.print("Start_Heartbeat,");
   pulseSensor.outputBeat();
   delay(20);
  }
  //--------------------------------------------------------------
//  //Acceleration Sensor 
//  sensors_event_t accel;
//  sensors_event_t gyro;
//  sensors_event_t temp;
//  sox.getEvent(&accel, &gyro, &temp);
//  //Serial.print("\n");
//  Serial.print("Amb_Temperature,"); // C
//  //Serial.print("\n");
//  Serial.print(temp.temperature);
//  //Serial.print("\n");  
//  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.print(",Accel_X,"); // m/s^2
//  //Serial.print("\n");
//  Serial.print(accel.acceleration.x);
//  //Serial.print("\n");
//  Serial.print(",Accel_Y,"); // m/s^2
//  //Serial.print("\n");
//  Serial.print(accel.acceleration.y);
//  //Serial.print("\n");
//  Serial.print(",Accel_Z,"); // m/s^2
//  //Serial.print("\n");
//  Serial.print(accel.acceleration.z);
//  //Serial.print("\n");
//  // /* Display the results (rotation is measured in rad/s) */
//  // Serial.print("Gyro X radians/s");
//  // Serial.print("\n");
//  // Serial.print(gyro.gyro.x);
//  // Serial.print("\n");
//  // Serial.print("Gyro Y radians/s ");
//  // Serial.print("\n");
//  // Serial.print(gyro.gyro.y);
//  // Serial.print("\n");
//  // Serial.print("Gyro Z radians/s ");
//  // Serial.print("\n");
//  // Serial.print(gyro.gyro.z);
//  // Serial.print("\n");  
//  delay(20);
  //--------------------------------------------------------------
  //Resistance and Volume code
  // Measure sensor resistance.
  float resistance = readResistance(SENSOR_PIN, SERIES_RESISTOR);
    //Serial.print("\n");
    // Serial.print(",Resistance,"); 
    //Serial.print("\n");
    // Serial.print(resistance, 2); // ohms
  // Map resistance to volume.
    float volume = resistanceToVolume(resistance, ZERO_VOLUME_RESISTANCE, CALIBRATION_RESISTANCE, CALIBRATION_VOLUME);
    // Convert the sensor reading to water level in mL
    waterLevel = map(volume, sensorMin, sensorMax, 0, maxWaterLevel); 
    Serial.print(",Volume,");
    //Serial.print("\n");
    Serial.print(volume, 5); // mL
    //Serial.print("\n");
    waterPercent = (volume/maxWaterLevel)*100;
    Serial.print(",W_Capacity_%,");
    Serial.print(waterPercent); // %

    // Modify the following lines to print the battery level and voltage in a readable format
    float battery_level = battery_read();
    Serial.print(",Battery_Voltage,");
    Serial.print(battery_level / 100 * (4.91 - 4.0) + 4.0, 2); // V
    // Serial.println("V");
    Serial.print(",Battery_Level_%,");
    Serial.print(battery_level, 2); // %
    // Serial.print("%, ");
}

  float battery_read()
  {
      //read battery voltage per %
      long sum = 0;                   // sum of samples taken
      float voltage = 0.0;            // calculated voltage
      float output = 0.0;             //output value
      const float battery_max = 4.91; //maximum voltage of battery
      const float battery_min = 4.0;  //minimum voltage of battery before shutdown
  
      for (int i = 0; i < 499; i++)
  {
      int reading = analogRead(battery_pin);
      sum += reading;
      //Serial.print("Reading ");
      //Serial.print(i);
      //Serial.print(": ");
      //Serial.println(reading);
      delayMicroseconds(100);
  }
      // calculate the voltage
      voltage = ((sum / (float)500));
      voltage = (((voltage*5.0)/1023)); //for default reference voltage
      //round value by two precision
     // voltage = roundf(voltage * 100) / 100;

      output = ((voltage - battery_min) / (battery_max - battery_min)) * 100;
      if (output < 100)
          return output;
      else
          return 100.0f;

      Serial.print(output);

    
  }
  float readResistance(int pin, int seriesResistance) 
  {
    // Get ADC value.
    float resistance = analogRead(pin);
    // Convert ADC reading to resistance.
    resistance = (1023.0 / resistance) - 1.0;
    resistance = seriesResistance / resistance;
    return resistance;
  }
  float resistanceToVolume(float resistance, float zeroResistance, float calResistance, float calVolume) {
    if (resistance > zeroResistance || (zeroResistance - calResistance) == 0.0) {
      // Stop if the value is above the zero threshold, or no max resistance is set (would be divide by zero).
      return 0.0;
    }
    // Compute scale factor by mapping resistance to 0...1.0+ range relative to maxResistance value.
  float scale = (zeroResistance - resistance) / (zeroResistance - calResistance);
    // Scale maxVolume based on computed scale factor.
    return calVolume * scale;  
     
  delay(20);

  
  
}
