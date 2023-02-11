import core, communicator
import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((core.SERVER,core.PORT))
server.listen()
print("Server listening on " + core.SERVER)

def handleClient():
    while True: 
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")
        print(f"onmt_translate -model {core.TRANSLATION_MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH + str(addr[-1])} -output {os.getcwd() + core.OUTPUT_PATH + str(addr[-1])}")
        while True:
            try:
                signal = communicator.receiveMessage(client, addr[-1])
                if signal == core.Operation['MT']:
                    os.environ['MKL_THREADING_LAYER'] = 'GNU'
                    os.system(f"onmt_translate -model {core.TRANSLATION_MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH + str(addr[-1])} -output {os.getcwd() + core.OUTPUT_PATH + str(addr[-1])}")
                elif signal == core.Operation['GEC']:
                    # Call model GEC here  
                    continue  
                else:
                    print(f"Error. Closing connection with {str(addr)}.")
                    client.close()
                    break
                communicator.sendMessage(client, addr[-1])
            except:
                print(f"Error. Closing connection with {str(addr)}.")
                client.close()
                break

handleClient()