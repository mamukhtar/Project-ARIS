import RPi.GPIO as GPIO
import time
import subprocess

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

# Turn on the red LED initially (system is off)
GPIO.output(27, GPIO.HIGH)
GPIO.output(17, GPIO.LOW)
print("System is off")

# Define a variable to keep track of the system state
system_on = False

# Define a variable to keep track of the process running the bash script
hub1_process = None

# Define a callback function to handle button press events
def button_callback(channel):
    global system_on, hub1_process
    if GPIO.input(channel):
        # Button is released
        if system_on:
            # Turn off the system (red LED on)
            GPIO.output(27, GPIO.HIGH)
            GPIO.output(17, GPIO.LOW)
            system_on = False
            print("System is off")
            if hub1_process is not None:
                # Kill the process running the Hub1.sh script
                hub1_process.kill()
                hub1_process = None
                print("Hub1.sh stopped")
        else:
            # Turn on the system (green LED on)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(17, GPIO.HIGH)
            system_on = True
            print("System is on")
            if hub1_process is None:
                # Start running the Hub1.sh script in a subprocess
                hub1_process = subprocess.Popen(['bash', '/home/sensor-hub1/Documents/Pi_codes/Hub1.sh'])
                print("Hub1.sh started")

# Register the button callback function to be called on button press events
GPIO.add_event_detect(26, GPIO.BOTH, callback=button_callback)

# Wait for button presses
while True:
    time.sleep(0.1)
