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

"""
This dictionary shows which languages that server supports in translation.
Add a new item 'lang_label': 'lang_fullname' into this dictionary if a new language is supported.
"""
SUPPORTED_LANGS = {
    'en': 'English',
    'de': 'German',
    'vi': 'Vietnamese'
}

"""
This tuple shows which (source language, target language) pairs that server supports in translation.
Add a new ('source_lang', 'target_lang') into this tuple if a new pair is supported.
"""
SUPPORTED_TRANS = (
    ('en', 'de'),
    ('en', 'vi')
)

BUFFER_SIZE = 4089
DELIMITER = '.'

INPUT_PATH = '/input/'
OUTPUT_PATH = '/output/'
EN_DE_TRANSLATION_MODEL_PATH = '/model/translation_model_ende_release.pt'
EN_VI_TRANSLATION_MODEL_PATH = '/model/translation_model_envi_release.pt'
GEC_MODEL_PATH = '/model/gec_model.pt'
EN_VI_SUBWORD_MODEL = '/model/en_vi.source.model'
EN_VI_DESUBWORD_MODEL = '/model/en_vi.target.model'
EN_DE_SUBWORD_MODEL = '/model/en_de.source.model'
EN_DE_DESUBWORD_MODEL = '/model/en_de.target.model'

LEN_PAD = 10
SIGNAL_PAD = 2
TRANS_PAD = 5
HEADER_BUFFER = LEN_PAD + SIGNAL_PAD + TRANS_PAD

PORT = 5555
SERVER_IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'