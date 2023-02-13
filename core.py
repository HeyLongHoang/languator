import socket

Operation = {
    'MT': '0',
    'GEC': '1',
    'DISCONNECT': '2'
}
Status = {
    'SUCCESS': 0,
    'FAILED': 1
}

BUFFER_SIZE = 4089
DELIMITER = '.'

INPUT_PATH = '/input/'
OUTPUT_PATH = '/output/'
TRANSLATION_MODEL_PATH = '/home/aiotlab3/RISE/YTrang/Languator/model/translation_model.pt'
GEC_MODEL_PATH = '/home/aiotlab3/RISE/YTrang/Languator/model/gec_model.pt'

LEN_PAD = 10
SIGNAL_PAD = 2
HEADER_BUFFER = LEN_PAD + SIGNAL_PAD

PORT = 5555
SERVER_IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
