/* This example demonstrates how to take a standard 3-wire pressure transducer
 *  and read the analog signal, then convert the signal to a readable output and
 *  display it onto an LCD screen.
 *  
 *  Contact Tyler at tylerovens@me.com if you have any questions
 */

#include "Wire.h" //allows communication over i2c devices
//#include "LiquidCrystal_I2C.h" //allows interfacing with LCD screens

const int pressureInput = A7; //select the analog input pin for the pressure transducer
const int pressureZero = 102.4; //analog reading of pressure transducer at 0psi
const int pressureMax = 921.6; //analog reading of pressure transducer at 100psi
const int pressuretransducermaxPSI = 100; //psi value of transducer being used
const int sensorreadDelay = 250; //constant integer to set the sensor read delay in milliseconds

float pressureValue = 0; //variable to store the value coming from the pressure transducer

//LiquidCrystal_I2C lcd(0x3f, 20, 4); //sets the LCD I2C communication address; format(address, columns, rows)

void setup() //setup routine, runs once when system turned on or reset
{
  Serial.begin(115200); //initializes serial communication at set baud rate bits per second
  //lcd.begin(); //initializes the LCD screen
}

void loop() //loop routine runs over and over again forever
{
  pressureValue = analogRead(pressureInput); //reads value from input pin and assigns to variable
  pressureValue = ((pressureValue-pressureZero)*pressuretransducermaxPSI)/(pressureMax-pressureZero); //conversion equation to convert analog reading to psi
  Serial.print(pressureValue, 1); //prints value from previous line to serial
  Serial.println("psi"); //prints label to serial
  //lcd.setCursor(0,0); //sets cursor to column 0, row 0
  //lcd.print("Pressure:"); //prints label
  //lcd.print(pressureValue, 1); //prints pressure value to lcd screen, 1 digit on float
  //lcd.print("psi"); //prints label after value
  //lcd.print("   "); //to clear the display after large values or negatives
  delay(sensorreadDelay); //delay in milliseconds between read values
}
