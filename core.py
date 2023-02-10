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

INPUT_PATH = '/home/aiotlab3/RISE/YTrang/Server-Python-Imaginator/input/'
OUTPUT_PATH = '/home/aiotlab3/RISE/YTrang/Server-Python-Imaginator/output/'
TRANSLATION_MODEL_PATH = '/home/aiotlab3/RISE/YTrang/AttentionNMT/run/luong/luong_attn_step_40000.pt'

LEN_PAD = 10
SIGNAL_PAD = 2
HEADER_BUFFER = LEN_PAD + SIGNAL_PAD

PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
