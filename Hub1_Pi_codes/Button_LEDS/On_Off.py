import RPi.GPIO as GPIO
import time

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

# Define a callback function to handle button press events
def button_callback(channel):
    global system_on
    if GPIO.input(channel):
        # Button is released
        if system_on:
            # Turn off the system (red LED on)
            GPIO.output(27, GPIO.HIGH)
            GPIO.output(17, GPIO.LOW)
            system_on = False
            print("System is off")
        else:
            # Turn on the system (green LED on)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(17, GPIO.HIGH)
            system_on = True
            print("System is on")

# Register the button callback function to be called on button press events
GPIO.add_event_detect(26, GPIO.BOTH, callback=button_callback)

# Wait for button presses
while True:
    time.sleep(0.1)
