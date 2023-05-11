import socket

server_ip = "10.0.0.173"
port = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))

while True:
    data = client.recv(61440)
    if not data:
        break

    print("Received data:", data[:4].decode('utf-8'), "Data size:", len(data) - 4)

client.close()
