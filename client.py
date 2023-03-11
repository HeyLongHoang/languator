import socket, time, os
import client_core as core

f = open('server_info.txt', 'r')
server_ipgen   = f.readline().strip()
server_port    = f.readline().strip()
server_address = f.readline().strip()
f.close()

core.SERVER_PORT = int(server_port)
if server_address == 'local':
    core.SERVER_IP = socket.gethostbyname(socket.gethostname())
else:
    core.SERVER_IP = server_address

class Client():
    def __init__(self, server_IP, server_port, IP_generation = server_ipgen):
        self.client = socket.socket()
        if IP_generation == 'IPv4':
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif IP_generation == 'IPv6':
            self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        self.srv_IP = server_IP
        self.srv_port = server_port
        self.srv_addr = (self.srv_IP, self.srv_port)

        self.connect()
        #self.handle_server()

    def connect(self):
        """Function to make connection with server"""
        try:
            self.client.connect(self.srv_addr)
        except Exception as e:
            print(e)

    def send_message(self, msg, signal, source_lang_no, target_lang_no):
        """Args:
            source_lang_no, target_lang_no - string of integer e.g: '0', '1', ...
        """
        try:
            msg_len = len(msg.encode(core.FORMAT))

            header = f'{msg_len:<{core.LEN_PAD}}'
            header += f'{signal:<{core.SIGNAL_PAD}}'
            header += f'{source_lang_no + target_lang_no:<{core.TRANS_PAD}}'

            self.client.send(header.encode(core.FORMAT))
            self.client.send(msg.encode(core.FORMAT))
        except Exception as e:
            print(e)

    def receive_message(self):
        """Function to get back the message from server"""
        try:
            header_rcv = self.client.recv(core.LEN_PAD).decode(core.FORMAT)
            print('Received header: ' + header_rcv)
            msg = self.client.recv(int(header_rcv)).decode(core.FORMAT)
            return msg
        except Exception as e:
            print(e)
            return None

    def reconnect(self):
        #TODO: reconnect if an error occurs
        pass

    def handle_server(self):
        """Function to test client"""
        signal = '-1'
        while True:
            # Input signal
            while signal not in core.Operation.values():
                print('Enter mode (0 - translation, 1 - correction, 2 - disconnect): ')
                signal = input()
            if signal == core.Operation['DISCONNECT']:
                self.client.close()
                break

            # Input string
            msg = input('Enter message: ')
            self.send_message(msg, signal)
            signal = '-1'
            print('Received from server: ' + self.receive_message())

