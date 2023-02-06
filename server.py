import core, communicator
import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((core.HOST_IP,core.HOST_PORT))
server.listen()
print("Server listening on " + core.HOST_IP)

def handleClient():
    while True: 
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")
        try:
            command = client.recv(1).decode()
            if command == core.Operation['MT']:
                communicator.receiveSentence(client)
                os.environ['MKL_THREADING_LAYER'] = 'GNU'
                os.system(f"onmt_translate -model {core.MODEL_PATH} -src {core.INPUT_PATH} -output {core.OUTPUT_PATH}")
                communicator.sendSentence(client)
            elif command == core.Operation['GEC']:
                continue
            else:
                print("Unrecognizable operation code, got " + command)
        except:
            print(f"Error. Closing connection with {str(addr)}.")
            client.close()

handleClient()