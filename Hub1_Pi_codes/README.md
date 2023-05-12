# Project README

Welcome to the repository containing a collection of programs designed for a distributed system. This README provides an overview of the programs included and their functionalities. Please refer to the individual program files for more detailed information, including setup instructions, dependencies, and usage guidelines.

1. **Arduino Program**:
   - This program is responsible for uploading integrated sensor code to the Arduino Nano. It ensures the proper functioning of the connected sensors.

2. **Arduino to Pi Program**:
   - The Arduino to Pi program reads sensor data from the Arduino board and saves it to a new CSV file every 200 sets of data. This ensures efficient data management and organization.

3. **Machine Learning Program**:
   - The Machine Learning Program processes the sensor data collected from the Arduino every 180 seconds. Using a pre-trained model, it analyzes the data and predicts the status and condition of the monitored environment. The program appends these predictions to the original sensor data, providing valuable insights.

4. **GPS Module and Journey Logistics Program**:
   - The GPS Module and Journey Logistics Program leverages GPS coordinates to calculate the distance, in kilometers and miles, from the current location to predefined buildings such as Wheatly, McCormick, Campus Center, University Hall, and others. Additionally, it estimates the time required to reach the destination based on GPS speed, assuming a walking speed of 3 miles per hour. The program also determines the consumables required for the journey, including oxygen, water, and battery. The calculated information is then appended to the full hub data file for comprehensive tracking and analysis.

5. **Hub-to-Hub Program**:
   - The Hub-to-Hub Program enables seamless communication between two hubs in the distributed system. It sends the full hub data file to the other hub every 180 seconds, dividing the data into manageable chunks of 200 bytes. In return, it receives the hub's full data file, which includes information about all astronauts. The received data is then saved locally for further analysis.

6. **Server-Client-UnityC Programs**:
   - The Server-Client-UnityC Programs consist of three components: the Python Client, the Server, and the Unity Client. The Python Client is responsible for sending hub 1 and hub 2 CSV data files to the server every 180 seconds. The Server receives and saves the data to separate folders for hub 1 and hub 2. The Unity Client receives the data sent by the server and saves it to specific folders within the Unity project's Assets directory. The data can then be utilized for visualization and display purposes within the Unity interface.

7. **Hub1/2 Bash Script**:
   - The Hub1/2 Bash Script orchestrates the execution of all the Python scripts in the background, ensuring the proper coordination of the different subsystems. It runs each script with specified time intervals between them. It's important to note that as some of the background processes are designed to run indefinitely, the script will not terminate until all the programs are manually stopped or the computer is rebooted. The off button does not terminate the script.

8. **On/Off Program**:
   - The On/Off Program is a Python script specifically designed to run on a Raspberry Pi computer. It provides functionality for starting and stopping the Hub1/2 Bash Script using a push button to toggle the state of the system on/off. Additionally, it utilizes LEDs to indicate the current state of the system, whether it's on or off. The script listens for button press events on a specific GPIO pin and, when the button is pressed, it toggles the state of the system on/off. It also starts and stops the bash script subprocess based on the current
