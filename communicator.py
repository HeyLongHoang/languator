import core
import os
import nltk.tokenize

def receiveCommand(client):
	try:
		command = ""
		print(f"Received command: "+ command)
		return command
	except Exception as e:
		print(e)
		return None

def receiveSentence(client):
	try:
		sentences = client.recv(core.BUFFER_SIZE).decode()
		if os.path.exists(core.INPUT_PATH):
			os.remove(core.INPUT_PATH)
		file = open(core.INPUT_PATH,'a')
		for x in nltk.tokenize.sent_tokenize(sentences):
			file.write(x)
			file.write('\n')
		file.close()
	except Exception as e:
		print(e)
		return None

def sendSentence(client):	
	try:
		file = open(core.OUTPUT_PATH,'r')
		output_data = file.read(core.BUFFER_SIZE).replace('\n', ' ')
		while output_data:
			client.send(output_data.encode())
			output_data = file.read(core.BUFFER_SIZE).replace('\n', ' ')
		print(f"Done sending output")
		file.close()
	except Exception as e:
		print(e)
		return None