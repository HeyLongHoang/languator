import socket,time,os
import core

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# I am,apparently, supposed to use 127.0.0.1 for the client and localhost for the server. Reasons unknown. Require additional data.
client.connect((core.HOST_IP,core.HOST_PORT))

# message = client.recv(core.BUFFER_SIZE)
# print("Received: " + message.decode())

reply = ''
while True:
    print("Type 0 for translation, 1 for grammar error corection:")
    reply = input()
    if (reply == '1' or reply == '0'):
        break
    else:
        print(f"Invalid option. Expected 1 or 0, instead got {reply}")
client.send(reply.encode())

print("Type your sentences here:")
reply = input()
client.send(reply.encode())

try: 
    result = '' + client.recv(core.BUFFER_SIZE).decode()
    print(result)
except Exception as e:
    print(e)

client.close()