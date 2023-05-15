int battery_pin = A2;

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
    delayMicroseconds(1000);
}
    // calculate the voltage
    voltage = ((sum / (float)500));
    voltage = (((voltage*5.0)/1023)); //for default reference voltage
    //round value by two precision
   // voltage = roundf(voltage * 100) / 100;
    Serial.print("voltage: ");
    Serial.println(voltage, 2);
    output = ((voltage - battery_min) / (battery_max - battery_min)) * 100;
    if (output < 100)
        return output;
    else
        return 100.0f;
}

void setup()
{
    analogReference(DEFAULT); //set reference voltage to internal
    Serial.begin(9600);
}

void loop()
{
    Serial.print("Battery Level: ");
    Serial.println(battery_read(), 2);
    delay(1000);
}
