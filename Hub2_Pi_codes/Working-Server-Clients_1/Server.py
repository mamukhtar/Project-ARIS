import socket
import threading
import os

class SensorServer:
    def __init__(self, host= '10.0.0.173', port=8000, hub1_dir='/Users/maryam/Desktop/Pi_codes/Working-Server-Clients/Hub1_data'):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.clients = []
        self.hub1_dir = hub1_dir
        
    def listen(self):
        self.sock.listen(5)
        print('Server listening on {}:{}'.format(self.host, self.port))
        
        while True:
            conn, addr = self.sock.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn,))
            client_thread.start()
            self.clients.append(conn)
            print('New client connected:', addr)
            
    def broadcast(self, data):
        for client in self.clients:
            try:
                client.send(data)
            except:
                self.clients.remove(client)
                
    def handle_client(self, conn):
        file_number = 0
        while True:
            data = conn.recv(61440)
            if not data:
                break

            if not os.path.exists(self.hub1_dir):
                os.makedirs(self.hub1_dir)

            filename = 'Hub1_sensor_data_{}.csv'.format(file_number)
            file_path = os.path.join(self.hub1_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(data)
            print('Received data from client')
            self.broadcast(data)
            file_number += 1

            
if __name__ == '__main__':
    server = SensorServer()
    server.listen()
