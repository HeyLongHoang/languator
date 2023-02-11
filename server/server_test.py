import socket
import os

import nltk
nltk.download('punkt')

"""
import torch
from happytransformer import TTSettings
args = TTSettings(num_beams=5, min_length=1)
gec_model = torch.load(server_core.GEC_MODEL_PATH)
"""

import server_core
#import communicator

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_core.SERVER_IP,server_core.SERVER_PORT))
server.listen()
print("Server listening on " + server_core.SERVER_IP)

def receiveMessage(conn, addr):
	try:
		header_rcv = conn.recv(server_core.HEADER_BUFFER).decode(server_core.FORMAT)
		print("Received header: " + header_rcv)
			# Receive header information
		msg_len = int(header_rcv[:server_core.LEN_PAD])
		signal = int(header_rcv[server_core.LEN_PAD:server_core.HEADER_BUFFER])
			
		# Receive input string
		msg = conn.recv(msg_len).decode(server_core.FORMAT)
		print("Received msg: " + msg)
			
		# Write sentences into input file 
		file = open(os.getcwd() + server_core.INPUT_PATH + str(addr),'a')
		for x in nltk.tokenize.sent_tokenize(msg):
			file.write(x)
			file.write('\n')
		file.close()
		print("Finished writing input.")
		return int(signal)
	except Exception as e:
		print(e)
		return 

def sendMessage(conn, addr):	
	try:
		# Open output file for the client, read it, then close
		file = open(os.getcwd() + server_core.INPUT_PATH + str(addr),'r')
		msg = file.read().replace('\n', ' ')
		file.close()

		# Send reply to client
		header = f'{len(msg.encode(server_core.FORMAT)):<{server_core.LEN_PAD}}'
		conn.send(header.encode(server_core.FORMAT))
		conn.send(msg.encode(server_core.FORMAT))
		print("Sent header: " + header)
		print("Sent message: " + msg)
		
		# Delete the output file after done sending
		os.remove(os.getcwd() + server_core.INPUT_PATH + str(addr))
		#os.remove(os.getcwd() + server_core.OUTPUT_PATH + str(addr))
		print("Finished removing input-output files.")
	except Exception as e:
		print(e)
		return None

def handleClient():
    while True: 
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")
        try:
            while(True):
                #signal = communicator.receiveMessage(client, addr[-1])
                signal = receiveMessage(client, addr[-1])
                if signal == server_core.Operation['MT']:
                    do_nothing = 0
                    # os.environ['MKL_THREADING_LAYER'] = 'GNU'
                    # os.system(f"onmt_translate -model {server_core.TRANSLATION_MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH + str(addr[-1])} -output {os.getcwd() + core.OUTPUT_PATH + str(addr[-1])}")
                elif signal == server_core.Operation['GEC']:
                    do_nothing = 0
                    """
                    # Open input and output file of the client
                    input_file = open(os.getcwd() + core.INPUT_PATH + str(addr[-1]),'r')
                    output_file = open(os.getcwd() + core.OUTPUT_PATH + str(addr[-1]),'a')
                    # For each sentence in the input file
                    for sentence in input_file.read().replace('\n', ' '):
                        # Get output from model
                        input = "grammar: " + sentence
                        output = gec_model.generate_text(input, args).text
                        print(output)
                        # Write into output file
                        output_file.write(output + '\n')
                    input_file.close()
                    output_file.close() 
                    """
                else:
                    print(f"Error. Closing connection with {str(addr)}.")
                    client.close()
                    
                #communicator.sendMessage(client, addr[-1])
                sendMessage(client, addr[-1])
        except:
            print(f"Error. Closing connection with {str(addr)}.")
            client.close()

handleClient()


















