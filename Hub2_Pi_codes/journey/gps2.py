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
import csv
from math import radians, cos, sin, asin, sqrt
import os

# for a computer, use the pyserial library for uart access
uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=10)

# Specify the directory path to save the CSV files
directory_path = "/home/sensor-hub2/Documents/Pi_codes/Hub2_data/"

# Specify the directory path to save the consumption CSV files
consu_directory_path = os.path.join(directory_path, "Hub2_consu_data")

# Create the consumption directory if it does not exist
if not os.path.exists(consu_directory_path):
    os.makedirs(consu_directory_path)
    print("Created Hub2_consu_data folder")

# Create a header row for the GPS data
gps_header = ["Timestamp", "Latitude", "Longitude", "Fix Quality", "Satellites", "Altitude (m)", "Speed (knots)", "Track Angle (deg)", "Horizontal Dilution", "Height Geoid (m)", "Distance to Destination (km)", "Time to Reach Destination (hours)", "Water Needed (L)", "Oxygen Needed (L)", "Battery Needed (%)", "Time to Consume Water (hours)", "Time to Consume Oxygen (hours)", "Time to Reach Target (hours)", "Destination"]

# Specify the maximum number of rows per file
max_rows_per_file = 200

# Initialize the row counter and file number for GPS data
gps_row_counter = 0
gps_file_number = 1

# Initialize the row counter and file number for consumption data
consu_row_counter = 0
consu_file_number = 1

# Latitude and longitude of the destination location
CC = (42.3126653, -71.0366086)
Uhall = (42.3131102, -71.0347790)
Wheatly = (42.3121882, -71.0382675)
ISC = (42.3141399, -71.0411653)
ResHall = (42.3165175, -71.0396415)
JfkStation = (42.3207083, -71.0522607)

destination1 = {"name": "CC", "lat": CC[0], "lon": CC[1]}
destination2 = {"name": "Uhall", "lat": Uhall[0], "lon": Uhall[1]}
destination3 = {"name": "Wheatly", "lat": Wheatly[0], "lon": Wheatly[1]}
destination4 = {"name": "ISC", "lat": ISC[0], "lon": ISC[1]}
destination5 = {"name": "ResHall", "lat": ResHall[0], "lon": ResHall[1]}
destination6 = {"name": "JfkStation", "lat": JfkStation[0], "lon": JfkStation[1]}

destinations = [destination1, destination2, destination3, destination4, destination5, destination6]


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

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

# Loop indefinitely
while True:
    # Check if it's time to create a new consumption file
    if consu_row_counter % max_rows_per_file == 0:
        # Create a new consumption file path
        consu_file_path = os.path.join(consu_directory_path, "Hub2_consu_data_{}.csv".format(consu_file_number))
        # Increment the consumption file number
        consu_file_number += 1
        # Reset the consumption row counter
        consu_row_counter = 0
        # Open the new consumption file in write mode and write the header row
        """with open(consu_file_path, mode='w', newline='') as consu_csv_file:
            consu_writer = csv.writer(consu_csv_file)
            consu_writer.writerow(gps_header)"""
    # Increment the consumption row counter
    consu_row_counter += 1
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

        # Calculate the distances from current coordinates to each destination.
        distances = {}
        for destination in destinations:
            distance = haversine(gps.longitude, gps.latitude, destination["lon"], destination["lat"])
            distances[destination["name"]] = distance
            print(f"Distance to {destination['name']}: {distance:.2f} km")

        # Find the closest destination
        closest_dest = min(distances, key=distances.get)
        dest_lon = next(item for item in destinations if item["name"] == closest_dest)["lon"]
        dest_lat = next(item for item in destinations if item["name"] == closest_dest)["lat"]

        # Calculate the time to reach each destination at normal walking speed of 3 miles per hour and at speed_knots
        walking_speed = 3.0 * 1.60934  # estimated speed in 3.0 m/h
        distances_speed_knots = {dest: distances[dest] / (gps.speed_knots * 1.852) for dest in distances}
        times_walk = {dest: distances[dest] / walking_speed for dest in distances}
        times_speed_knots = {dest: distances_speed_knots[dest] / gps.speed_knots for dest in distances}

        # Print the results
        print("=" * 40)
        print("Closest destination:", closest_dest)
        print("Walking speed:")
        for dest, time in times_walk.items():
            print(f"Time to reach walking {dest}: {time:.2f} hours")
        print("Speed in knots:")
        for dest, time in times_speed_knots.items():
            print(f"Time to reach {dest}: {time:.2f} hours")

        # Consumption rates per unit distance and time
        water_rate = 0.5 # liters per kilometer
        oxygen_rate = 0.1 # liters per kilometer
        battery_rate = 0.05 # percent per kilometer

        # Calculate the distances and consumables for each destination
        for destination in destinations:
            # Calculate the distance to the current destination
            dest_distance = haversine(gps.longitude, gps.latitude, destination["lon"], destination["lat"])
            print(f"Distance to {destination['name']}: {dest_distance:.2f} km")

            # Calculate the amount of water, oxygen, and battery needed for the current destination
            water_needed = water_rate * dest_distance
            oxygen_needed = oxygen_rate * dest_distance
            battery_needed = battery_rate * dest_distance

            # Calculate the time required to consume the water and oxygen needed
            water_time = water_needed / water_rate
            oxygen_time = oxygen_needed / oxygen_rate


            # Print the results
            print(f"Water needed for {destination['name']}: {water_needed:.2f} liters")
            print(f"Oxygen needed for {destination['name']}: {oxygen_needed:.2f} liters")
            print(f"Battery needed for {destination['name']}: {battery_needed:.2f}%")
            print(f"Time to consume water for {destination['name']}: {water_time:.2f} hours")
            print(f"Time to consume oxygen for {destination['name']}: {oxygen_time:.2f} hours")
            print()

        # Write the header row to the first consumption file
        with open(consu_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                "Time",
                "Latitude",
                "Longitude",
                "Fix quality",
                "Satellites",
                "Altitude (m)",
                "Speed (knots)",
                "Track angle (deg)",
                "Horizontal dilution",
                "Height geoid",
                "Destination",
                "Distance to destination (km)",
                "Time to reach destination (h)",
                "Water needed (l)",
                "Oxygen needed (l)",
                "Battery needed (%)",
                "Time to consume water (h)",
                "Time to consume oxygen (h)",
                "Time to reach target (h)"
            ])

        # Check if it's time to create a new consumption file
        if consu_row_counter % max_rows_per_file == 0:
            # Create a new consumption file path
            consu_file_path = os.path.join(consu_directory_path, "Hub2_consu_data_{}.csv".format(consu_file_number))
            # Increment the consumption file number
            consu_file_number += 1
            # Reset the consumption row counter
            consu_row_counter = 0

        # Write the GPS data to the current file
        with open(consu_file_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                gps.latitude,
                gps.longitude,
                gps.fix_quality,
                gps.satellites,
                gps.altitude_m,
                gps.speed_knots,
                gps.track_angle_deg,
                gps.horizontal_dilution,
                gps.height_geoid,
                closest_dest,
                dest_distance,
                water_needed,
                oxygen_needed,
                battery_needed,
                water_time,
                oxygen_time,
            ])

        # Increment the consumption row counter
        consu_row_counter += 1

        print("All coordinates processed.")


