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
		msg_len, signal, lang1, lang2 = process_header(header_rcv)
			
		# Receive input string
		msg = conn.recv(msg_len).decode(core.FORMAT)
		print("Received msg: " + msg)
			
		# Write sentences into input file 
		file = open(os.getcwd() + core.INPUT_PATH + str(addr),'a')
		for x in nltk.tokenize.sent_tokenize(msg):
			file.write(x + '\n')
		file.close()
		print("Finished writing input.")
		
		return str(signal), lang1, lang2
	except Exception as e:
		print(e)
		return None
	
def process_header(header):
	'''
	Returns:
	msg_len -- int, length of message
	signal -- int, task value, 0 for MT, 1 for GEC
	lang1, lang2 -- integer of type string for MT, space string for GEC
	'''
	msg_len = int(header[:core.LEN_PAD])
	signal = int(header[core.LEN_PAD : core.LEN_PAD + core.SIGNAL_PAD]) # get integer value
	langs = header[core.LEN_PAD + core.SIGNAL_PAD : core.HEADER_BUFFER]
	lang1, lang2 = langs[:core.LANG_LABEL_SIZE], langs[core.LANG_LABEL_SIZE : 2 * core.LANG_LABEL_SIZE]
	return msg_len, signal, lang1, lang2

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