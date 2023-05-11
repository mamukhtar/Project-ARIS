import serial
import time, csv, os
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import *

# Enable USB Communication
Tx1_PORT = '/dev/ttyUSB1'  # Tx1 xbee port 
Rx2_PORT = '/dev/ttyUSB0'  # Rx2 xbee port
BAUD_RATE = 9600  # baudrate
data_counter = 0

 # Set the initial file number to 0
file_num = 1
file_name2 = f"sensor_data_{file_num}.csv"

Tx1_RECEIVER = "Rx1_xbee2"  # the NI node identifier of the transmitter xbeee
Tx2_TRANSMITTER = "Tx2_xbee3"  # the NI node identifier of the transmitter xbeee

def main():
    file_num = 3
    count = 1 # count number of transmissions

    print("XBee Transmiter Test 1")
    Tx1_device = XBeeDevice(Tx1_PORT, BAUD_RATE)
    Rx2_device = XBeeDevice(Rx2_PORT, BAUD_RATE)
    try:
        Tx1_device.open()
        Rx2_device.open()

        xbee_network = Tx1_device.get_network()
        remote_dev = xbee_network.discover_device(Tx1_RECEIVER)
        xbee_network_2 = Rx2_device.get_network()
        Tx2_remote_dev = xbee_network_2.discover_device(Tx2_TRANSMITTER)

        if remote_dev is None:
            print("Remote device receiver for HUB 1 not found")
            exit(1)

        if Tx2_remote_dev is None:
            print("Remote device transmitter for HUB 2 not found")
            exit(1)

        Rx2_device.add_data_received_callback(my_data_received_callback)

        while True:
            # Generate the file name based on the file number
            file_name = f"/home/sensor-hub1/Documents/Pi_codes/Hub1_data/Hub1_sensor_data_{file_num}.csv"

            # Read the CSV file and send the data
            CHUNK_SIZE = 200  # number of bytes to send at a time
            with open(file_name, "rb") as f:
                data = f.read()
                num_chunks = len(data) // CHUNK_SIZE + (1 if len(data) % CHUNK_SIZE > 0 else 0)

                for i in range(num_chunks):
                    chunk = data[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
                    print("Sending chunk %d of %d to %s..." % (i+1, num_chunks, remote_dev.get_64bit_addr()))
                    Tx1_device.send_data(remote_dev, chunk)
                    time.sleep(0.1)

            print(f"Sent all data %s", (count))
            # Increment the file number after each file is sent
            file_num += 1
            # Wait for 3 minutes before sending the next file
            time.sleep(180)
            # method to receive data 
            Rx2_device.add_data_received_callback(my_data_received_callback)
            time.sleep(2)

    except TimeoutException:
        if remote_dev is not None:
            print("Timeout occured, communication failed with %s \n", remote_dev.get_64bit_addr())
        else:
            print("Timeout occured, communication failed with an unknown remote device \n")

    except InvalidOperatingModeException:
        print("Operating mode of %s is not API or API-escape \n", remote_dev.get_64bit_addr())

    except XBeeException:
        print("Device %s may be closed or error occured when writing to it \n", remote_dev.get_64bit_addr())

    finally:
        if Tx1_device is not None and Tx1_device.is_open():
            Tx1_device.close()

def my_data_received_callback(xbee_message):
    global data_counter
    global file_num
    global file_name2
    
    address = xbee_message.remote_device.get_64bit_addr()
    data = xbee_message.data.decode("utf8")
    print("Data received from %s: %s" % (address, data))
    
    if not os.path.exists("Hub2_data"):
        os.makedirs("Hub2_data")
        print("Created Hub2_data folder")

    with open(os.path.join("Hub2_data", file_name2), "a") as f:
        f.write(data)
        data_counter += 1
        if data_counter == 200:
            f.close()
            file_num = len(os.listdir("Hub2_data"))
            file_name2 = "Hub2_sensor_data_%d.csv" % file_num
            data_counter = 0


if __name__ == '__main__':
    main()
