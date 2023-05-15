# Importing required modules
import socket
import time
import os
from contextlib import closing

# Initialize the SensorClient class
class SensorClient:
    # Constructor of the SensorClient class
    def __init__(self, host=None, port=9000):
        # Set the host IP address, if provided; otherwise, get the local IP address
        self.host = host if host else self.get_local_ip_address()  
        self.port = port  # Set the port number
        # Create a socket object for the TCP/IP communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.file_num_1 = 0  # Initialize the file number for directory 1
        self.file_num_2 = 0  # Initialize the file number for directory 2

    # Connect to a remote IP address to get the local IP address of the server
    def get_local_ip_address(self):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('10.255.255.255', 1))
                # Get the local IP address from the socket
                local_ip = s.getsockname()[0]
            except:
                # If an exception is raised, use the loopback IP address
                local_ip = '127.0.0.1'
            finally:
                s.close() # Close the socket
            return local_ip # Return the local IP address
        
    # Connect to the server
    def connect(self):
        while True:
            try:
                # Connect to the server with the provided IP address and port number
                self.sock.connect((self.host, self.port))  
                print('Connected to server')
                break
            except:
                print('Connection failed. Retrying in 5 seconds...')
                time.sleep(5)
    
    # Get the filename and the corresponding filename (fn) of a data file in directory 1
    def get_filename_1(self):
        # Generate the filename with the current file number for Hub 1 directory
        filename_1 = f"/home/sensor-hub2/Documents/Pi_codes/Hub1_data/Hub1_sensor_data_{self.file_num_1}.csv"  
        fn1 = os.path.basename(filename_1)  # Get the filename of the data file
        self.file_num_1 += 1  # Increment the file number for directory 1
        return filename_1, fn1

    # Get the filename and the corresponding filename (fn) of a data file in directory 2
    def get_filename_2(self):
        # Generate the filename with the current file number for Hub 2 directory
        filename_2 = f"/home/sensor-hub2/Documents/Pi_codes/Hub2_data/Hub2_sensor_data_{self.file_num_2}.csv"  
        fn2 = os.path.basename(filename_2)  # Get the filename of the data file
        self.file_num_2 += 1  # Increment the file number for directory 2
        return filename_2, fn2
    
    # Send a data file from directory 1 to the server
    def send_file1(self, filename_1):
        with open(filename_1, 'rb') as f:
            data_1 = f.read()  # Read the binary data from the file
        hub_prefix = b'Hub1'  # Add a prefix to the data to identify the source of the data (directory 1)
        message = hub_prefix + data_1  # Concatenate the prefix and the data
        self.sock.sendall(message)  # Send the message to the server
        x = len(data_1)  # Get the number of bytes in the data
        print(f'{x} bytes sent for file {os.path.basename(filename_1)}') 

    # Send a data file from directory 2 to the server
    def send_file2(self, filename_2):
        with open(filename_2, 'rb') as f:
            data_2 = f.read()  # Read the binary data from the file
        hub_prefix = b'Hub2'  # Add a prefix to the data to identify the source of the data (directory 2)
        message = hub_prefix + data_2  # Concatenate the prefix and the data
        self.sock.sendall(message)  # Send the message to the server
        x = len(data_2)  # Get the number of bytes in the data
        print(f'{x} bytes sent for file {os.path.basename(filename_2)}')
            
# Main execution block
if __name__ == '__main__':
    client = SensorClient()  # Create a SensorClient object
    client.connect()  # Connect to the server
    while True:
        # Get the filename and the corresponding filename (fn) of a data file in directory 1
        filename_1, fn1 = client.get_filename_1()
        # Get the filename and the corresponding filename (fn) of a data file in directory 2
        filename_2, fn2 = client.get_filename_2()  
        try:
            client.send_file1(filename_1)  # Send the data file from Hub 1 directory to the server
            print(f'File {fn1} sent successfully')
        except:
            print(f'Error sending file {fn1}. Retrying in 5 seconds...')
        try:
            client.send_file2(filename_2)  # Send the data file from Hub 2 directory to the server
            print(f'File {fn2} sent successfully')
        except:
            print(f'Error sending file {fn2}. Retrying in 5 seconds...')
        time.sleep(60)  # Wait for 60 seconds before sending the next data file
else:
    print("Server not found.")


