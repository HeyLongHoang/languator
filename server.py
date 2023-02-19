import core, communicator, subword
import socket
import threading
import os
import torch
from happytransformer import TTSettings

args = TTSettings(num_beams=5, min_length=1)
gec_model = torch.load(os.getcwd() + core.GEC_MODEL_PATH)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((core.SERVER_IP,core.PORT))
server.listen()
print("Server listening on " + core.SERVER_IP)

def doServerStuff(client, addr):
    while True:
            try:
                signal, lang1, lang2 = communicator.receiveMessage(client, addr[-1])
                if signal == core.Operation['MT']:
                    translate(lang1, lang2, addr[-1])
                elif signal == core.Operation['GEC']:
                    # Open input and output file of the client
                    input_file = open(os.getcwd() + core.INPUT_PATH + str(addr[-1]),'r')
                    output_file = open(os.getcwd() + core.OUTPUT_PATH + str(addr[-1]),'a')
                    # For each sentence in the input file
                    for sentence in input_file.readlines():
                        sentence = sentence.replace('\n','')
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

def translate(lang1, lang2, addr):
    if lang1 == core.LANG_STOI['en'] and lang2 == core.LANG_STOI['de']:
        os.environ['MKL_THREADING_LAYER'] = 'GNU'
        subword.subword(os.getcwd() + core.EN_DE_SUBWORD_MODEL, os.getcwd() + core.INPUT_PATH + str(addr))
        os.system(f"onmt_translate -model {os.getcwd() + core.EN_DE_TRANSLATION_MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH + str(addr)} -output {os.getcwd() + core.OUTPUT_PATH + str(addr)}")
        subword.desubword(os.getcwd() + core.EN_DE_DESUBWORD_MODEL, os.getcwd() + core.OUTPUT_PATH + str(addr))
    elif lang1 == core.LANG_STOI['en'] and lang2 == core.LANG_STOI['vi']:
        os.environ['MKL_THREADING_LAYER'] = 'GNU'
        subword.subword(os.getcwd() + core.EN_VI_SUBWORD_MODEL, os.getcwd() + core.INPUT_PATH + str(addr))
        os.system(f"onmt_translate -model {os.getcwd() + core.EN_VI_TRANSLATION_MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH + str(addr)} -output {os.getcwd() + core.OUTPUT_PATH + str(addr)}")
        subword.desubword(os.getcwd() + core.EN_VI_DESUBWORD_MODEL, os.getcwd() + core.OUTPUT_PATH + str(addr))
    else:
        return None

def handleClient():
    while True: 
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")

        thread = threading.Thread(target=doServerStuff, args=(client,addr))
        thread.start()

handleClient()
