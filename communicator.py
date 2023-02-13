import core
import os
import nltk.tokenize

def receiveMessage(conn, addr):
	try: 
		header_rcv = conn.recv(core.HEADER_BUFFER).decode(core.FORMAT)
		if header_rcv:
			print("Received header: " + header_rcv)
		else:
			return None
		# Receive header information
		msg_len = int(header_rcv[:core.LEN_PAD])
		signal = int(header_rcv[core.LEN_PAD:core.HEADER_BUFFER]) # get integer value
			
		# Receive input string
		msg = conn.recv(msg_len).decode(core.FORMAT)
		print("Received msg: " + msg)
			
		# Write sentences into input file 
		file = open(os.getcwd() + core.INPUT_PATH + str(addr),'a')
		for x in nltk.tokenize.sent_tokenize(msg):
			file.write(x + '\n')
		file.close()
		print("Finished writing input.")
		return str(signal) # cast to become string value
	except Exception as e:
		print(e)
		return None

def sendMessage(conn, addr):	
	try:
		# Open output file for the client, read it, then close
		file = open(os.getcwd() + core.OUTPUT_PATH + str(addr),'r')
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
		os.remove(os.getcwd() + core.OUTPUT_PATH + str(addr))
		print("Finished removing input-output files.")
	except Exception as e:
		print(e)
		return None