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

LANG_STOI = {
    'en': '0',
    'de': '1',
    'vi': '2'
}

LANG_ITOS = {
    i:s for s,i in LANG_STOI.items()
}

LANG_LABEL_SIZE = len(list(LANG_STOI.values())[0]) 
# size of encoded language value e.g '0' has size 1

SUPPORT_TRANS = (
    ('en', 'de'),
    ('en', 'vi')
)

LANG_CONNECT = {
    'en': 'English',
    'de': 'German',
    'vi': 'Vietnamese'
}

BUFFER_SIZE = 4089
DELIMITER = '.'

INPUT_PATH = '/input/'
OUTPUT_PATH = '/output/'
EN_DE_TRANSLATION_MODEL_PATH = '/Users/longhoang/Downloads/translation_model_release.pt'
EN_VI_TRANSLATION_MODEL_PATH = '/Users/longhoang/Downloads/translation_model_envi_release.pt'
GEC_MODEL_PATH = '/Users/longhoang/Developer/Python/ML/DL_projects/GEC/gec_model.pt'

LEN_PAD = 10
SIGNAL_PAD = 2
TRANS_PAD = 5
HEADER_BUFFER = LEN_PAD + SIGNAL_PAD + TRANS_PAD

PORT = 5555
SERVER_IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
