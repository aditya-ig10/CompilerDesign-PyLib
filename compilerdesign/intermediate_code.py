"""
Intermediate Code Generation: Postfix (RPN), Prefix, and Infix expression conversion.
"""

PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
RIGHT_ASSOC = {'^'}


def _tokenize(expr: str) -> list:
    tokens = []
    i = 0
    expr = expr.strip()
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue
        if expr[i].isalnum() or expr[i] == '_':
            j = i
            while j < len(expr) and (expr[j].isalnum() or expr[j] == '_' or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            tokens.append(expr[i])
            i += 1
    return tokens


def _validate_non_empty(expr: str) -> None:
    if not expr or not expr.strip():
        raise ValueError("Expression cannot be empty.")


def infix_to_postfix(expr: str) -> str:
    _validate_non_empty(expr)
    tokens = _tokenize(expr)
    output = []
    stack = []

    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
        elif token in PRECEDENCE:
            while (stack and stack[-1] != '(' and
                   stack[-1] in PRECEDENCE and
                   (PRECEDENCE[stack[-1]] > PRECEDENCE[token] or
                    (PRECEDENCE[stack[-1]] == PRECEDENCE[token] and token not in RIGHT_ASSOC))):
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(output)


def infix_to_prefix(expr: str) -> str:
    _validate_non_empty(expr)
    tokens = _tokenize(expr)
    reversed_tokens = []
    for t in reversed(tokens):
        if t == '(':
            reversed_tokens.append(')')
        elif t == ')':
            reversed_tokens.append('(')
        else:
            reversed_tokens.append(t)

    output = []
    stack = []

    for token in reversed_tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
        elif token in PRECEDENCE:
            while (stack and stack[-1] != '(' and
                   stack[-1] in PRECEDENCE and
                   (PRECEDENCE[stack[-1]] > PRECEDENCE[token] or
                    (PRECEDENCE[stack[-1]] == PRECEDENCE[token] and token in RIGHT_ASSOC))):
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(reversed(output))


def postfix_to_infix(expr: str) -> str:
    _validate_non_empty(expr)
    tokens = expr.strip().split()
    stack = []

    for token in tokens:
        if token in PRECEDENCE:
            if len(stack) < 2:
                raise ValueError(f"Invalid postfix expression: not enough operands for '{token}'")
            b = stack.pop()
            a = stack.pop()
            stack.append(f"({a} {token} {b})")
        else:
            stack.append(token)

    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    return stack[0]


def prefix_to_infix(expr: str) -> str:
    _validate_non_empty(expr)
    tokens = expr.strip().split()
    stack = []

    for token in reversed(tokens):
        if token in PRECEDENCE:
            if len(stack) < 2:
                raise ValueError(f"Invalid prefix expression: not enough operands for '{token}'")
            a = stack.pop()
            b = stack.pop()
            stack.append(f"({a} {token} {b})")
        else:
            stack.append(token)

    if len(stack) != 1:
        raise ValueError("Invalid prefix expression")
    return stack[0]


def postfix_to_prefix(expr: str) -> str:
    return infix_to_prefix(postfix_to_infix(expr))


def prefix_to_postfix(expr: str) -> str:
    return infix_to_postfix(prefix_to_infix(expr))


def convert_expression(expr: str, from_notation: str, to_notation: str) -> str:
    _validate_non_empty(expr)
    from_notation = from_notation.lower()
    to_notation = to_notation.lower()

    if from_notation == to_notation:
        return expr

    converters = {
        ('infix', 'postfix'): infix_to_postfix,
        ('infix', 'prefix'): infix_to_prefix,
        ('postfix', 'infix'): postfix_to_infix,
        ('postfix', 'prefix'): postfix_to_prefix,
        ('prefix', 'infix'): prefix_to_infix,
        ('prefix', 'postfix'): prefix_to_postfix,
    }

    key = (from_notation, to_notation)
    if key not in converters:
        raise ValueError(f"Unsupported conversion: {from_notation} -> {to_notation}")

    return converters[key](expr)
