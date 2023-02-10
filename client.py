import socket,time,os
import core


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# I am,apparently, supposed to use 127.0.0.1 for the client and localhost for the server. Reasons unknown. Require additional data.
client.connect((core.SERVER,core.PORT))

# message = client.recv(core.BUFFER_SIZE)
# print("Received: " + message.decode())

# reply = ''
# while True:
#     print("Type 0 for translation, 1 for grammar error corection:")
#     reply = input()
#     if (reply == '1' or reply == '0'):
#         break
#     else:
#         print(f"Invalid option. Expected 1 or 0, instead got {reply}")
# client.send(reply.encode())

# print("Type your sentences here:")
# reply = input()
# client.send(reply.encode())

# try: 
#     result = '' + client.recv(core.BUFFER_SIZE).decode()
#     print(result)
# except Exception as e:
#     print(e)

# client.close()

def send_message(msg, signal):
    try:
        msg_encoded = msg.encode(core.FORMAT)
        msg_len = len(msg_encoded)

        # add length of message to header
        header = str(msg_len).encode(core.FORMAT)
        header += b' '*(core.LEN_PAD - len(header)) # pad with spaces

        # add signal value to header
        header += str(signal).encode(core.FORMAT)
        header += b' '*(core.HEADER_BUFFER - len(header))

        client.send(header)
        client.send(msg_encoded)
    except Exception as e:
        print(e)

def receive_message():
    """
    Function to get back the message from server
    """
    try:
        header_rcv = client.recv(core.LEN_PAD).decode(core.FORMAT)
        msg = client.recv(int(header_rcv)).decode(core.FORMAT)
        return msg
    except Exception as e:
        print(e)
        return None
# loop to accept new messages
signal = -1
while True:
    # input signal
    while signal not in core.Operation.values():
        print("Enter mode (0 - translation, 1 - correction, 2 - disconnect): ")
        signal = str(input())
    if signal == core.Operation['DISCONNECT']:
        client.close()
        break
       
    # input string
    msg = input("Enter message: ")
    send_message(msg, signal)
    signal = -1
    print("Received from server: " + receive_message())

