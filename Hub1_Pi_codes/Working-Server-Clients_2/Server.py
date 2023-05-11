import socket
import threading
import os

class SensorServer:
    def __init__(self, host=None, port=8000, 
                 hub1_dir='/home/sensor-hub1/Documents/Pi_codes/Working-Server-Clients_2/Hub1_data', 
                 hub2_dir='/home/sensor-hub1/Documents/Pi_codes/Working-Server-Clients_2/Hub2_data'):
        # If no host is provided, use the local IP address of the server
        if not host:
            host = self.get_local_ip()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Add this line to allow port reuse
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.clients = []  # A list to keep track of connected clients
        self.hub1_dir = hub1_dir  # Path to directory where data from directory 1 (Hub1) will be saved
        self.hub2_dir = hub2_dir  # Path to directory where data from directory 2 (Hub2) will be saved

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]  # Get the local IP address of the server
        except:
            ip = '127.0.0.1'  # Use localhost if IP address cannot be obtained
        finally:
            s.close()
        return ip
        
    def listen(self):
        self.sock.listen(5)  # Listen for incoming connections
        print('Server listening on {}:{}'.format(self.host, self.port))
        
        while True:
            conn, addr = self.sock.accept()  # Accept a new connection
            client_thread = threading.Thread(target=self.handle_client, args=(conn,))
            client_thread.start()  # Create a new thread to handle the connection
            self.clients.append(conn)  # Add the connection to the list of connected clients
            print('New client connected:', addr)
            
    def broadcast(self, data):
        for client in self.clients:
            try:
                # Send data to all connected clients
                client.send(data) 
            except:
                # Remove the client from the list if the connection is lost
                self.clients.remove(client)  

    def handle_client(self, conn):
        # A dictionary to keep track of the file numbers for each directory
        file_numbers = {'Hub1': 0, 'Hub2': 0}  
        while True:
            try:
                data = conn.recv(61440)  # Receive data from the client
                print('Received data from Python Client Hub 1')
                if not data:
                    break

                hub_prefix = data[:4].decode('utf-8')  # Extract the hub prefix from the data
                if hub_prefix not in file_numbers:
                    print('Unknown hub prefix:', hub_prefix)
                    continue

                hub_dir = self.hub1_dir if hub_prefix == 'Hub1' else self.hub2_dir

                if not os.path.exists(hub_dir):
                    os.makedirs(hub_dir)
                
                # Generate a filename based on the hub prefix and file number
                filename = '{}_sensor_data_{}.csv'.format(hub_prefix, file_numbers[hub_prefix])  
                file_path = os.path.join(hub_dir, filename)  # Get the full file path
                # Write the data to the file, The data after the first 4 bytes (hub prefix) is the content of the CSV file
                # The file is written in binary mode ('wb')
                # This will overwrite the file if it already exists
                with open(file_path, 'wb') as f:
                    f.write(data[4:]) 

                print('Sent data to Client', filename)

                # Broadcast data to connected clients
                self.broadcast(data)
                # Increment the file number for the current hub prefix
                file_numbers[hub_prefix] += 1
            except Exception as e:
                print(f'Error handling client: {e}')
                conn.close()
                break

if __name__ == '__main__':
    server = SensorServer()
    server.listen() # Start the server and listen for incoming connections
