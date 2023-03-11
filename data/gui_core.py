import client_core

MIN_WIDTH       = 1200
MIN_HEIGHT      = 600

FUNCTION_LIST   = ['NULL', 'Translator', 'Grammar Checker', 'NULL', 'NULL']
FUNCTION        = ['NULL', 'TRANSLATE',  'CHECK GRAMMAR',   'NULL', 'NULL']
FUNCTION_RESULT = ['NULL', 'TRANSLATED', 'GRAMMAR CHECKED', 'NULL', 'NULL']

DEFAULT_OUTPUT  = ['',
                   'Translation',
                   'Nothing to check yet!\nStart writing or pasting something on the editor to begin.',
                   '',
                   ''
                   ]

LANGUAGES_LABEL = list(client_core.SUPPORTED_LANGS.keys())
LANGUAGES       = list(client_core.SUPPORTED_LANGS.values())

SUPPORTED_TRANS = client_core.SUPPORTED_TRANS

ERROR_NOTIF     = {'connection_prob'     : 'Something went wrong. Please check your internet connection and try again later.',
                   'unsupported_lang_01' : 'Currently the program hasn\'t supported in translation from ',
                   'unsupported_lang_02' : ' to ',
                   'unsupported_lang_03' : ' yet. We\'ll update this feature soon.'
                   }

ICONS           = {'swap-dark'  : './data/icons/horizontal-arrows-symbolic-dark-theme.svg',
                   'swap-light' : './data/icons/horizontal-arrows-symbolic-light-theme.svg',
                   'light-mode' : './data/icons/sun-outline-symbolic.svg'
                   }
