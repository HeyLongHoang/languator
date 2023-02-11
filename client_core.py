import socket

Operation = {
    'MT': 0,
    'GEC': 1,
    'DISCONNECT': 2
}
Status = {
    'SUCCESS': 0,
    'FAILED': 1
}

BUFFER_SIZE = 4089
DELIMITER = '.'

LEN_PAD = 10
SIGNAL_PAD = 2
HEADER_BUFFER = LEN_PAD + SIGNAL_PAD

SERVER_PORT = 5051
SERVER_IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
