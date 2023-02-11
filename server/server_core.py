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

INPUT_PATH = '/input/'
OUTPUT_PATH = '/output/'
TRANSLATION_MODEL_PATH = '/home/aiotlab3/RISE/YTrang/AttentionNMT/run/rnn/avg_attn_step_80000.pt'
GEC_MODEL_PATH = '/home/daonguyen/Projects/Languator/languator-ytrang-01/gec_model.pt'


LEN_PAD = 10
SIGNAL_PAD = 2
HEADER_BUFFER = LEN_PAD + SIGNAL_PAD

SERVER_PORT = 5051
SERVER_IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
