import core, communicator
import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((core.SERVER_IP,core.PORT))
server.listen()
print("Server listening on " + core.SERVER_IP)

def receiveMessage(conn, addr):
	try:
		header_rcv = conn.recv(core.HEADER_BUFFER).decode(core.FORMAT)
		print("Received header: " + header_rcv)
		# Receive header information
		msg_len = int(header_rcv[:core.LEN_PAD])
		signal = int(header_rcv[core.LEN_PAD:core.HEADER_BUFFER])
			
		# Receive input string
		msg = conn.recv(msg_len).decode(core.FORMAT)
		print("Received msg: " + msg)
			
		# Write sentences into input file 
		file = open(os.getcwd() + core.INPUT_PATH + str(addr),'a')
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
		file = open(os.getcwd() + core.INPUT_PATH + str(addr),'r')
		msg = file.read().replace('\n', ' ')
		file.close()

		# Send reply to client
		header = f'{len(msg.encode(core.FORMAT)):<{core.LEN_PAD}}'
		conn.send(header.encode(core.FORMAT))
		conn.send(msg.encode(core.FORMAT))
		print("Sent header: " + header)
		print("Sent message: " + msg)
		
		# Delete the output file after done sending
		os.remove(os.getcwd() + core.INPUT_PATH + str(addr))
		#os.remove(os.getcwd() + core.OUTPUT_PATH + str(addr))
		print("Finished removing input-output files.")
	except Exception as e:
		print(e)
		return None

def handleClient():
    while True:
        client, addr = server.accept()
        print(f"Connected with {str(addr)}.")
        while True:
            try:	
                signal = communicator.receiveMessage(client, addr[-1])
                if signal == core.Operation['MT']:
                    continue
                    # os.environ['MKL_THREADING_LAYER'] = 'GNU'
                    # os.system(f"onmt_translate -model {core.TRANSLATION_MODEL_PATH} -src {os.getcwd() + core.INPUT_PATH + str(addr[-1])} -output {os.getcwd() + core.OUTPUT_PATH + str(addr[-1])}")
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