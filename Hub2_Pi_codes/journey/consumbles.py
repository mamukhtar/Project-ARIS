# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
import time
import board
import busio
import adafruit_gps
import serial
from math import radians, cos, sin, asin, sqrt
import sys
sys.path.append('/home/sensor-hub2/Documents/Pi_codes/ML')

# for a computer, use the pyserial library for uart access
uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=10)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")

# Latitude and longitude of the destination location
dest_lat = 42.3126653
dest_lon = -71.0366086

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            continue
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print("=" * 40)  # Print a separator line.
        print(
            "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                gps.timestamp_utc.tm_mday,  # struct_time object that holds
                gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                gps.timestamp_utc.tm_min,  # month!
                gps.timestamp_utc.tm_sec,
            )
        )
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
        print("Fix quality: {}".format(gps.fix_quality))

        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print("# satellites: {}".format(gps.satellites))
        if gps.altitude_m is not None:
            print("Altitude: {} meters".format(gps.altitude_m))
        if gps.speed_knots is not None:
            print("Speed: {} knots".format(gps.speed_knots))
        if gps.track_angle_deg is not None:
            print("Track angle: {} degrees".format(gps.track_angle_deg))
        if gps.horizontal_dilution is not None:
            print("Horizontal dilution: {}".format(gps.horizontal_dilution))
        if gps.height_geoid is not None:
            print("Height geoid: {} meters".format(gps.height_geoid))

            # Calculate distance and time to destination location
        dest_distance = haversine(gps.longitude, gps.latitude, dest_lon, dest_lat)
        dest_distance_miles = dest_distance * 0.621371

        print("Distance to destination: {:.2f} km".format(dest_distance))
        print("Distance to destination: {:.2f} miles".format(dest_distance_miles))

        # Calculate the time to reach the destination at normal walking speed of 3 miles per hour
        if gps.speed_knots is None or gps.speed_knots != 0:
            dest_time = dest_distance / (gps.speed_knots * 1.60934)
            print("Time to reach destination: {:.2f} hours".format(dest_time))
        else:
            dest_time = "Unknown"
            if gps.speed_knots is not None:
                print("Speed is not available")
            else:
                print("dest_time = ", dest_time)

        # Calculate the estimated time to reach the target location
        speed = (3.0 * 1.60934) #  estimated speed in 3.0 m/h
        time_to_reach = dest_distance / speed
        print(f'Time to reach target: {time_to_reach:.2f} hour')

        #import the machine learning code
        import ML
        dataset = ML.new_file_path
        activity = ML.predicted_label
        status = ML.condition

        water_level=dataset['Volume']
        oxygen_level=dataset['Pressure']
        battery_level=dataset['Battery_Level_%']

        # Consumables equations
        if activity == 'resting':
            intensity_factor = 1
        elif activity == 'walking':
            intensity_factor = 1.5
        elif activity == 'running':
            intensity_factor = 2

        water_needed= 15.772*time_to_reach*intensity_factor
        oxygen_needed= 12*0.36*time_to_reach*intensity_factor
        battery_level_needed=(18 + 13)*time_to_reach / 60 / 38 * 100

        # consumables left over
        water_consumed=water_level-water_needed
        oxygen_consumed=oxygen_level-oxygen_needed
        battery_level_remaining=battery_level-battery_level_needed

