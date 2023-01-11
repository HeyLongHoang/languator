from time import sleep
from turtle import width
import core, communicator, imaginator
import socket, cv2
import numpy as np


server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.bind((core.HOST_IP,core.HOST_PORT))
server.listen()
print("Server listening on " + core.HOST_IP)

def handleClient():
    while True: 
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")
        try:
            dataType, color, flip, crop = communicator.receiveCommand(client)
            if dataType == core.DataType['IMAGE']:
                handleImage(client, color, flip, crop)
                print("Sending procesed image to client")
                communicator.sendImage(client)
            else:
                handleVideo(client, color, flip, crop)
                print("Sending procesed video to client")
                communicator.sendVideo(client)
        except:
            print(f"Closing connection with {str(addr)}.")
            client.close()

def handleImage(client, color, flip, crop):
    image = communicator.receiveImage(client)
    try:
        file = open(core.ORIGINAL_IMAGE, 'wb')
        file.write(image)
        file.close()
        print("Received image has been saved in the server")
    except:
        print(f"Problem opening file {core.ORIGINAL_IMAGE}")
        return None
    
    imaginator.processImg(core.ORIGINAL_IMAGE,core.GENERATED_IMAGE,color,crop,flip)
    print("Image has been processed")


def handleVideo(client, color, flip, crop):
    video = communicator.receiveVideo(client)

    try:
        file = open(core.ORIGINAL_VIDEO, 'wb')
        file.write(video)
        file.close()
        print("Received video has been saved in the server")
    except:
        print(f"Problem opening file {core.ORIGINAL_VIDEO}")
        return None
    
    imaginator.processVideo(core.ORIGINAL_VIDEO,core.GENERATED_VIDEO,color,crop,flip,40)
    print("Video has been processed")

handleClient()