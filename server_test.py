primport core
import socket, os
import numpy as np


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((core.SERVER,core.PORT))
server.listen()
print("Server listening on " + core.SERVER)

def handleClient():
    while True: #Run accept method all the time. If a client connects, get its socket and address
        client, addr = server.accept()
        print(type(addr))
        print(f"Connected with {str(addr)}.")

        message = "Hello this is server"
        try:
            client.send(message.encode())

            reply = client.recv(core.BUFFER_SIZE)
            print("Received: " + reply.decode())

            client.close()
        except Exception as e:
            print(e)
            client.close()
        
        
os.system(f"onmt_translate -model {core.MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH} -output {os.getcwd() + core.OUTPUT_PATH}")
#handleClient()