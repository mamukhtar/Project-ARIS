#!/bin/bash

# Function to stop all child processes
function stop_child_processes {
  echo "Stopping child processes..."
  pids=$(pgrep -P $$) # get the PIDs of all child processes
  for pid in $pids; do
    kill $pid # kill each child process
  done
}

# Trap the SIGINT signal
trap 'stop_child_processes' SIGINT

# python3 /home/sensor-hub2/Documents/Pi_codes/A_Pi/Sensor_csv.py &
# sleep 150s
python3 /home/sensor-hub2/Documents/Pi_codes/ML/AR_Assistant_ML.py &
sleep 20s
python3 /home/sensor-hub2/Documents/Pi_codes/journey/gps2.py &
sleep 10s
python3 /home/sensor-hub2/Documents/Pi_codes/hub-to-hub/hub2tohub1.py &
sleep 180s
python3 /home/sensor-hub2/Documents/Pi_codes/Working-Server-Clients_2/Server.py &
sleep 5s
python3 /home/sensor-hub2/Documents/Pi_codes/Working-Server-Clients_2/Client.py &
wait
