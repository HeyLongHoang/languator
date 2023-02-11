import core, communicator
import socket
import os
import torch
from happytransformer import TTSettings

args = TTSettings(num_beams=5, min_length=1)
gec_model = torch.load(core.GEC_MODEL_PATH)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((core.SERVER_IP,core.PORT))
server.listen()
print("Server listening on " + core.SERVER_IP)


def handleClient():
    while True: 
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")
        
        while True:
            try:
                signal = communicator.receiveMessage(client, addr[-1])
                if signal == core.Operation['MT']:
                    os.environ['MKL_THREADING_LAYER'] = 'GNU'
                    os.system(f"onmt_translate -model {core.TRANSLATION_MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH + str(addr[-1])} -output {os.getcwd() + core.OUTPUT_PATH + str(addr[-1])}")
                elif signal == core.Operation['GEC']:
                    # Open input and output file of the client
                    input_file = open(os.getcwd() + core.INPUT_PATH + str(addr[-1]),'r')
                    output_file = open(os.getcwd() + core.OUTPUT_PATH + str(addr[-1]),'a')
                    # For each sentence in the input file
                    for sentence in input_file.read().replace('\n', ' '):
                        # Get output from model
                        input = "grammar: " + sentence
                        output = gec_model.generate_text(input, args).text
                        # Write into output file
                        output_file.write(output + '\n')
                    input_file.close()
                    output_file.close()
                else:
                    print(f"Client closed connection {str(addr)}.")
                    break
                communicator.sendMessage(client, addr[-1])
            except:
                print(f"Error. Closing connection with {str(addr)}.")
                client.close()
                break

handleClient()