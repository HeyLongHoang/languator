import socket,time,os
import core

buffsize = 1024
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # I am,apparently, supposed to use 127.0.0.1 for the client and localhost for the server. Reasons unknown. Require additional data.
client.connect(('127.0.0.1',5555))

counter = 0
file = open('TestClient.mp4','wb')
img_data = client.recv(core.BUFFER_SIZE)
data = bytearray()
while len(img_data) >= 0:
    #client.send(img_data)
    counter += 1
    data.extend(img_data)
    img_data = client.recv(core.BUFFER_SIZE)

file.write(data)
file.close()    
client.close()