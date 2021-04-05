import regex


def map_lang2code(code, lang):
    if lang in available_languages:
        for k, v in from_lang2code[lang].items():
            expr = rf'({k})(?!\w)'
            code = regex.sub(expr, v, code)
        return code
    else:
        return ""


def map_code2lang(code, lang):
    if lang in available_languages:
        for k, v in from_code2lang[lang].items():
            if k in code:
                code = code.replace(k, v)
        return code
    else:
        return ""


# key: in the language; item: in native code (to be implemented as wild-card values)
# native_code will be english in the meanwhile

from_en2code = {'sets': 'sets',
                'applies': 'applies',
                'outputs': 'outputs',
                'inputs': 'inputs',
                'maps': 'maps',
                'uses': 'uses',
                'adds': 'adds',
                'loads': 'loads',
                'keeps': 'keeps',
                'parallels': 'parallels',
                'publishes': 'publishes',
                'invokes': 'invokes',
                'divides': 'divides',
                'powers': 'powers',
                'consumes': 'consumes',
                'moves': 'moves',
                'waits': 'waits',
                'checks': 'checks',
                'returns': 'returns',
                'multiplies': 'multiplies',
                'where': 'where',
                'as': 'as',
                'with': 'with',
                'if': 'if',
                'else': 'else',
                'null': 'null',
                'void': 'void',
                'none': 'none',
                'true': 'true',
                'false': 'false',
                'string': 'string',
                'boolean': 'boolean',
                'hexadecimal': 'hexadecimal',
                'binary': 'binary',
                'real': 'real'
                }

from_code2en = {v: k for k, v in from_en2code.items()}

from_pt2code = {'seta': 'sets',
                'aplica': 'applies',
                'apresenta': 'outputs',
                'recebe': 'inputs',
                'mapeia': 'maps',
                'usa': 'uses',
                'adiciona': 'adds',
                'carrega': 'loads',
                'mantém': 'keeps',
                'paraleliza': 'parallels',
                'publica': 'publishes',
                'invoca': 'invokes',
                'divide': 'divides',
                'eleva': 'powers',
                'consome': 'consumes',
                'move': 'moves',
                'aguarda': 'waits',
                'checa': 'checks',
                'retorna': 'returns',
                'multiplica': 'multiplies',
                'onde': 'where',
                'como': 'as',
                'com': 'with',
                'se': 'if',
                'senão': 'else',
                'nulo': 'null',
                'vazio': 'void',
                'nada': 'none',
                'verdadeiro': 'true',
                'falso': 'false',
                'string': 'string',
                'booleano': 'boolean',
                'hexadecimal': 'hexadecimal',
                'binário': 'binary',
                'real': 'real'
                }

from_code2pt = {v: k for k, v in from_pt2code.items()}

available_languages = [None, 'en', 'pt']
from_lang2code = {'en': from_en2code, 'pt': from_pt2code, None: from_en2code}
from_code2lang = {'en': from_code2en, 'pt': from_code2pt, None: from_code2en}

highlighting = {'actions': (['names',
                            'loads',  #
                            'inputs',  #
                            'outputs',  #
                            'reads',  #
                            'applies',  #
                            'starts',
                            'divides',  #
                            'powers',  #
                            'maps',  #
                            'adds',  #
                            'multiplies',  #
                            'keeps',  #
                            'publishes',  #
                            'invokes',  #
                            'dequeues',  #
                            'queues',  #
                            'parallels',  #
                            'processes',
                            'threads',
                            'produces',  #
                            'consumes',  #
                            'uses',  #
                            'roots',
                            'sets',  #
                            'brings',
                            'calls',
                            'waits',  #
                            'moves',  #
                            'resets',  #
                            'repeats',
                            'executes',  #
                            'checks',  #
                            'evaluates',
                            'computes',
                            'defines',
                            'compares',
                            'loops',
                            'returns',  #
                            'translates'], '#9080ff') ,
                'complements': (['with', 'where', 'as', 'if', 'else', 'at'], '#7c3737'),
                'quantum': (['qubit'], '#92008c'),
                'elements': (['\:', '@', '\&', '\|',], '#ff9b57'),
                'symbols': (['\%', '\=', '\=\=', '\!\=', '<>', '~\=', '\>', '\<', '\>\=', '\=\>', '\<\=',
                            '\=\<'], '#f09d68'),  #'#e6ccff'),
                'loop': (['\$', '\_', '\.\.\.'], '#92008c'),
                'attr_types': (['string', 'real', 'boolean', 'binary', 'hexadecimal', 'qubin',
                               'null', 'none', 'void'], '#dd0000'),
                'comment': ([r'(\#\#.*\#\#|\/\*.*\*\/|\/\/.*\/\/)'], '#c9e7e7'),
                'misc': ([r'\[', r'\]', r'」', r'』', r'「', r'『', r'\(', r'\)', r'（', r'）'], '#D0D0D0'),
                'extra': ([r'(true|false)', r'0b[0-1]+', r'0x[a-fA-F0-9]+', r'((?!(0[xb]))[+-]?(\d+([.]{1}\d+)?([eE][+-]+(\d+([.]{1}\d*)?))?|[.]{1}\d+([eE][+-]+(\d+([.]{1}\d+)?))))'], '#26c5c9'),
                'string': ([r'(\".*?\"|«.*?»|„.*?“)'], '#218766')
                }
