# Import necessary libraries
import serial
import csv
import os
import time
from datetime import datetime
import pytz

# Set up the serial connection to the Arduino ls /dev | grep ttyUSB
arduino_port = "/dev/ttyUSB2"
baud = 115200 #arduino nano runs at 115200 baud
ser = serial.Serial(arduino_port, 115200, timeout=1)

# Print a message indicating that we are connected to the Arduino
print("Connected to Arduino port:" + arduino_port)

# Set the timezone to Eastern Standard Time
est = pytz.timezone('US/Eastern')

fieldnames = ['Time', 'Sensor1a', 'Amb_Temp', 'Sensor1b', 'Accel_X', 'Sensor1c', 'Accel_Y', 'Sensor1d','Accel_Z', 
              'Sensor2a', 'Volume', 'Sensor2b', 'Volume_%', 'Sensor3a', 'Batttery_V', 'Sensor3b', 'Batttery_Level_%', 'Sensor4a',
              'Pressure', 'Sensor4b', 'Pressure_%', 'Sensor5a', 'Body_Temp_C', 'Sensor5b', 'Body_Temp_F', 'Sensor6a',
              'Heart_rate', 'BPM', 'IBI']

# Define the folder name
folderName = "Hub1_data"

# Create the folder if it doesn't exist
if not os.path.exists(folderName):
    os.makedirs(folderName)

# Define the name and fieldnames of the CSV file that will store the data
fileName = "Hub1_sensor_data.csv"
filePath = os.path.join(folderName, fileName)


# Initialize variables for tracking the line count and maximum number of lines
line_count = 0
file_count = 0
max_lines = 200 # set the maximum number of lines before replacing the CSV file

# Continuously read data from the serial port
while True:
    # Read a line of text from the serial port and decode it as a UTF-8 string
    line = ser.readline().decode('utf-8').strip()

    # Get the current time in Eastern Standard Time and format it as a string
    time_str = datetime.now(est).strftime('%Y-%m-%d %H:%M:%S')

    # Split the line of text into individual data fields and prepend the current time
    data = [time_str] + line.split(',')

    # Write the data to the CSV file
    # with open('sensor_data.csv', 'a', newline='') as csvfile:
    with open(filePath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if line_count == 0: # If this is the first line in the file, write the header
            writer.writerow(fieldnames)
        writer.writerow(data)
    
    line_count += 1


    # Check if we have reached the maximum number of lines
    if line_count >= max_lines:
        # Rename the old file with a timestamp and create a new file with the same name
        fileName2 = os.path.join(folderName, 'Hub1_sensor_data_' + str(file_count) + '.csv')
        os.rename(filePath, fileName2)
        # fileName2 = os.rename('sensor_data.csv', 'sensor_data_' + str(file_count) + '.csv')
        line_count = 0
        file_count += 1
    print("Data Saved")

    # Check if the file is more than 10 minutes old
    if os.path.exists(fileName):
        file_creation_time = os.path.getctime(fileName)
        current_time = time.time()
        if (current_time - file_creation_time) > 300:
            os.remove(fileName)
            print(f"Deleted old file {fileName}")

