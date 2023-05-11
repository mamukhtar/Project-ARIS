import socket
import time

class SensorClient:
    def __init__(self, host= '10.0.0.173', port=8000):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_num = 0
        
    def connect(self):
        while True:
            try:
                self.sock.connect((self.host, self.port))
                break
            except:
                print('Connection failed. Retrying in 5 seconds...')
                time.sleep(5)
        
    def send_file(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
        self.sock.sendall(data)
        x = len(data)
        print(x)
        
    def get_filename(self):
        filename = f"/Users/maryam/Desktop/Pi_codes/A_Pi/Hub1_data/Hub1_sensor_data_{self.file_num}.csv"
        self.file_num += 1
        return filename
        
if __name__ == '__main__':
    client = SensorClient()
    client.connect()
    while True:
        filename = client.get_filename()
        try:
            client.send_file(filename)
            print(f'File {filename} sent successfully')
        except:
            print(f'Error sending file {filename}. Retrying in 5 seconds...')
        time.sleep(60)
