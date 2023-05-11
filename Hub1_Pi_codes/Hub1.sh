#!/bin/bash
# make it executable - chmod +x Hub1.sh
# to run it - ./Hub1.sh

# Function to stop all child processes
function stop_child_processes {
  echo "Stopping child processes..."
  pkill -P $$
}

# Trap the SIGINT signal
trap 'stop_child_processes' SIGINT

# python3 /home/sensor-hub1/Documents/Pi_codes/A_Pi/Sensor_csv.py &
# sleep 150s
python3 /home/sensor-hub1/Documents/Pi_codes/ML/ML.py &
sleep 20s
python3 /home/sensor-hub1/Documents/Pi_codes/journey/consumbles.py &
sleep 10s
python3 /home/sensor-hub1/Documents/Pi_codes/hub-to-hub/hub1tohub2.py &
sleep 180s
python3 /home/sensor-hub1/Documents/Pi_codes/Working-Server-Clients_2/Server.py &
sleep 5s
python3 /home/sensor-hub1/Documents/Pi_codes/Working-Server-Clients_2/Client.py &
wait
