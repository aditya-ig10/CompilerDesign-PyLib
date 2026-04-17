import re
from collections import Counter

from ._utils import sorted_unique

KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
    'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
    'volatile', 'while', 'include', 'define', 'printf', 'scanf', 'main'
}

OPERATORS = set('+-*/%=<>!&|^~?:')
PUNCTUATION = set('(){};,.[]\'"')


def lexical_analyzer(code: str) -> dict:
    """
    Perform lexical analysis on given source code.

    Returns a dict with:
      - tokens: list of (token_type, value) tuples
      - summary: counts of each token type
      - characters: total character count (excl. whitespace)
    """
    tokens = []
    pattern = r'\".*?\"|\'.*?\'|\/\/.*|\/\*[\s\S]*?\*\/|\d+\.\d+|\d+|[a-zA-Z_]\w*|[^\s]'
    raw_tokens = re.findall(pattern, code)

    for t in raw_tokens:
        if t.startswith('//') or t.startswith('/*'):
            tokens.append(('COMMENT', t))
        elif t.startswith('"') or t.startswith("'"):
            tokens.append(('STRING_LITERAL', t))
        elif re.fullmatch(r'\d+\.\d+', t):
            tokens.append(('FLOAT_CONSTANT', t))
        elif re.fullmatch(r'\d+', t):
            tokens.append(('INTEGER_CONSTANT', t))
        elif re.fullmatch(r'[a-zA-Z_]\w*', t):
            if t in KEYWORDS:
                tokens.append(('KEYWORD', t))
            else:
                tokens.append(('IDENTIFIER', t))
        elif all(c in OPERATORS for c in t):
            tokens.append(('OPERATOR', t))
        elif t in PUNCTUATION:
            tokens.append(('PUNCTUATION', t))
        else:
            tokens.append(('UNKNOWN', t))

    type_counts = Counter(ttype for ttype, _ in tokens)
    char_count = len(re.sub(r'\s', '', code))

    identifiers = [v for ttype, v in tokens if ttype == 'IDENTIFIER']
    keywords_found = [v for ttype, v in tokens if ttype == 'KEYWORD']
    token_stream = [
        {
            'index': index,
            'type': token_type,
            'value': value,
        }
        for index, (token_type, value) in enumerate(tokens, start=1)
    ]

    return {
        'tokens': tokens,
        'token_stream': token_stream,
        'summary': {
            'total_tokens': len(tokens),
            'total_characters': char_count,
            'total_lines': code.count('\n') + 1,
            'keywords': type_counts.get('KEYWORD', 0),
            'identifiers': type_counts.get('IDENTIFIER', 0),
            'integer_constants': type_counts.get('INTEGER_CONSTANT', 0),
            'float_constants': type_counts.get('FLOAT_CONSTANT', 0),
            'operators': type_counts.get('OPERATOR', 0),
            'punctuation': type_counts.get('PUNCTUATION', 0),
            'string_literals': type_counts.get('STRING_LITERAL', 0),
            'comments': type_counts.get('COMMENT', 0),
            'unknown': type_counts.get('UNKNOWN', 0),
        },
        'unique_identifiers': sorted_unique(identifiers),
        'keywords_used': sorted_unique(keywords_found),
    }
