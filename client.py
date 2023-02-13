import socket,time,os
import core

class Client():
    def __init__(self, server_IP, server_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.srv_IP = server_IP
        self.srv_port = server_port
        self.srv_addr = (self.srv_IP, self.srv_port)

        self.connect()
        self.handle_server()
    
    '''Function to make connection with server'''
    def connect(self):
        try:
            self.client.connect(self.srv_addr)
        except Exception as e:
            print(e)

    def send_message(self, msg, signal):
        try:
            msg_len = len(msg.encode(core.FORMAT))

            header = f'{len(msg):<{core.LEN_PAD}}'
            header += f'{signal:<{core.SIGNAL_PAD}}'

            self.client.send(header.encode(core.FORMAT))
            self.client.send(msg.encode(core.FORMAT))
        except Exception as e:
            print(e)

    def receive_message(self):
        """
        Function to get back the message from server
        """
        try:
            header_rcv = self.client.recv(core.LEN_PAD).decode(core.FORMAT)
            print("Received header: " + header_rcv)
            msg = self.client.recv(int(header_rcv)).decode(core.FORMAT)
            return msg
        except Exception as e:
            print(e)
            return None
    
    def handle_server(self):
        signal = -1
        while True:
            # input signal
            while signal not in core.Operation.values():
                print("Enter mode (0 - translation, 1 - correction, 2 - disconnect): ")
                signal = input()
            if signal == core.Operation['DISCONNECT']:
                self.client.close()
                break
            
            # input string
            msg = input("Enter message: ")
            self.send_message(msg, signal)
            signal = -1
            print("Received from server: " + self.receive_message())

