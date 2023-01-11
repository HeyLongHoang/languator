import core
import os

def receiveCommand(client):
	try:
		command = client.recv(9)[2:].decode('utf-8').split(core.DELIMITER)
		command = [int(i) for i in command]
		print(f"Received command: Type = {command[0]} | Color = {command[1]} | Flip = {command[2]} | Crop = {command[3]}")

		return command
	except Exception as e:
		print(e)
		return None


def receiveImage(client):
	try:
		# metadata = client.recv(8)[2:].decode('utf-8')
		# metadata = [int(i) for i in metadata]
		# print(f"Received image info: Length = {metadata[0]}")

		image = bytearray()
		received = client.recv(4)
		length = int.from_bytes(received,"big")
		
		counter = 0
		while counter < length:
			received = client.recv(core.BUFFER_SIZE)
			image.extend(received)
			counter += len(received)
		print(f"Received image: Length = {len(image)}")

		return image
	except Exception as e:
		print(e)
		return None

def sendImage(client):
	counter = 0
	metadata = str(os.path.getsize(core.GENERATED_IMAGE)) + '\n'
	try:
		print(f"Sending {metadata.encode()}")
		client.send(metadata.encode())
	except:
		print("Problem sending image metadata")
		
	try:
		file = open(core.GENERATED_IMAGE,'rb')
		img_data = file.read(core.BUFFER_SIZE)
		while img_data:
			client.send(img_data)
			counter += 1
			#print(f'Sent package {counter}')
			img_data = file.read(core.BUFFER_SIZE)
		print(f"Done sending {counter} packages of the image")
		file.close()
	except Exception as e:
		print(e)
		return None
	
def receiveVideo(client):
	try:
		video = bytearray()
		received = client.recv(4)
		length = int.from_bytes(received,"big")
		
		counter = 0
		while counter < length:
			received = client.recv(core.BUFFER_SIZE)
			video.extend(received)
			counter += len(received)
		print(f"Received video: Length = {counter}")
		return video
	except Exception as e:
		print(e)
		return None

def sendVideo(client):
	counter = 0
	metadata = str(os.path.getsize(core.GENERATED_VIDEO)) + '\n'
	print(f"Sending {metadata.encode()}")
	try:
		client.send(metadata.encode())
	except:
		print("Problem sending video metadata")
		
	try:
		file = open(core.GENERATED_VIDEO,'rb')
		vid_data = file.read(core.BUFFER_SIZE)
		while vid_data:
			client.send(vid_data)
			counter += 1
			if counter%50 == 0:
				print(f'Sent package {counter}')
			vid_data = file.read(core.BUFFER_SIZE)
		print(f"Done sending {counter} packages of the video")
		file.close()
	except:
		print(f"Problem opening file {core.GENERATED_VIDEO}")
		return None
