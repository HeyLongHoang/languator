from time import sleep
from turtle import width
import core, communicator, imaginator
import socket, cv2
import numpy as np


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((core.HOST_IP,core.HOST_PORT))
server.listen()
print("Server listening on " + core.HOST_IP)

def handleClient():
    while True: #Run accept method all the time. If a client connects, get its socket and address
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")

        try:
            communicator.sendVideo(client)
            client.close()
        except Exception as e:
            print(e)
            client.close()
        
        

handleClient()