# Project-ARIS
A collection of programs for sensor data processing, machine learning, GPS integration, and hub-to-hub communication in a distributed system.
# Project README

This README provides an overview of the components and programs included in this GitHub repository. The repository contains various programs related to sensor data processing, machine learning, GPS journey logistics, hub-to-hub communication, server-client communication, and a Unity project for the HoloLens interface. The programs are designed to work together to facilitate data collection, analysis, and communication for ARIS an Augmented reality Informational system for astronauts. Below is a brief description of each program:

1. **Arduino Program**:
   - Uploads integrated sensors code to the Arduino Nano to allow for continuous data collection.
   - Code Written by Oussama with help from Maryam to organize the data output 
   
2. **Arduino to Pi Program**:
   - Reads sensor data from the Arduino and saves it to a new CSV file every 200 sets of data.
   - Code Written by Maryam
   
3. **Machine Learning Program**:
   - Takes the read sensor data every 180 seconds, applies machine learning techniques, and determines the status and condition based on the training set if the data is Normal or Abnormal given the status i.e. running, walking or resting. The results are appended to the original sensor data.
   - Code Written by Kalvin with help from Maryam
   
4. **GPS Module and Journey Logistics Program**:
   - Calculates the distance in kilometers and miles from the current location to predefined buildings using GPS coordinates.
   - Estimates the time required to reach the destination based on GPS speed and assumes a walking speed of 3 miles per hour.
   - Determines the consumables (oxygen, water, and battery) needed for the journey and appends the information to the full hub data file.
   - Code Written by Maryam and Kalvin
   
5. **Hub-to-Hub Program**:
   - Sends the full hub data file to the other hub in chunks of 200 bytes every 180 seconds.
   - Receives the full appended data file from the other hub and saves it locally.
   - Code Written by Maryam
   
6. **Server-Client-UnityC Programs**:
   - The Python client sends hub 1 and hub 2 CSV data files to the server every 180 seconds.
   - The server saves the received data files to separate folders for hub 1 and hub 2.
   - The Unity client receives the data and saves it to folders within the Unity project's Assets directory for display purposes.
   - Code Written by Maryam
   
7. **Hub1/2 Bash Script**:
   - Executes a sequence of Python scripts in the background with specified time intervals.
   - Some of the background processes run in an infinite loop, so the script continues until all programs are manually stopped or the computer is rebooted.
   -  Code Written by Maryam
   
8. **On/Off Program**:
   - Designed to run on a Raspberry Pi computer, this Python script controls the state of the system with a push button.
   - The script listens for button press events on a specific GPIO pin and toggles the system on/off accordingly.
   - LEDs are used to indicate the state of the system.
   - Additionally, the script starts and stops the hub1/2 bash script as per the system's state.
   -  Code Written by Maryam

Please refer to the individual program files for more detailed information, including specific setup instructions, dependencies, and usage guidelines.

Feel free to explore and utilize these programs according to your project requirements. If you have any questions or encounter any issues, please don't hesitate to reach out to us.

Enjoy working with the system!

-*Maryam Aminu Mukhtar (CE) Team Lead, 
Oussama Ourich (EE) Co-Team Lead,
Felice Gabardi (EE),
Kalvin Fonseca (EE),
/Team 4*
