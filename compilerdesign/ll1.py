"""
LL(1) Predictive Parsing Table construction and parsing.
"""

from ._utils import EPSILON, normalize_grammar, stringify_symbols
from .first_follow import compute_first, compute_follow

END_MARKER = '$'


def build_ll1_table(grammar: dict, start: str = None) -> dict:
    """
    Build the LL(1) predictive parsing table.
    """
    grammar = normalize_grammar(grammar)
    if start is None:
        start = next(iter(grammar))

    first_sets = compute_first(grammar)
    follow_sets = compute_follow(grammar, start)

    table = {}
    conflicts = []

    def first_of_string(symbols):
        result = set()
        for sym in symbols:
            if sym in grammar:
                sym_first = set(first_sets[sym])
            else:
                sym_first = {sym}
            result.update(sym_first - {EPSILON})
            if EPSILON not in sym_first:
                break
        else:
            result.add(EPSILON)
        return result

    for A, productions in grammar.items():
        for prod in productions:
            symbols = prod.strip().split()
            first_prod = first_of_string(symbols) if symbols != [EPSILON] else {EPSILON}

            for terminal in first_prod - {EPSILON}:
                key = (A, terminal)
                if key in table:
                    conflicts.append(f"Conflict at ({A}, {terminal}): '{table[key]}' vs '{prod}'")
                else:
                    table[key] = prod

            if EPSILON in first_prod:
                for terminal in follow_sets[A]:
                    key = (A, terminal)
                    if key in table:
                        conflicts.append(f"Conflict at ({A}, {terminal}): '{table[key]}' vs '{prod}'")
                    else:
                        table[key] = prod

    sorted_entries = [
        {
            'non_terminal': non_terminal,
            'terminal': terminal,
            'production': production,
        }
        for (non_terminal, terminal), production in sorted(table.items())
    ]

    return {
        'table': table,
        'entries': sorted_entries,
        'conflicts': sorted(conflicts),
        'is_ll1': len(conflicts) == 0
    }


def ll1_parse(grammar: dict, tokens: list, start: str = None) -> dict:
    """
    Parse a list of tokens using LL(1) predictive parsing.
    """
    grammar = normalize_grammar(grammar)
    if start is None:
        start = next(iter(grammar))

    result = build_ll1_table(grammar, start)
    table = result['table']

    input_tokens = tokens + [END_MARKER]
    stack = [END_MARKER, start]
    idx = 0
    steps = []
    error = None

    while stack:
        top = stack[-1]
        current = input_tokens[idx] if idx < len(input_tokens) else END_MARKER

        step = {
            'step': len(steps) + 1,
            'stack': list(reversed(stack)),
            'input': input_tokens[idx:],
            'stack_display': stringify_symbols(reversed(stack)),
            'input_display': stringify_symbols(input_tokens[idx:]),
            'action': ''
        }

        if top == END_MARKER and current == END_MARKER:
            step['action'] = 'ACCEPT'
            steps.append(step)
            break
        elif top == current:
            step['action'] = f'Match {top}'
            steps.append(step)
            stack.pop()
            idx += 1
        elif top in grammar:
            key = (top, current)
            if key in table:
                prod = table[key]
                step['action'] = f'{top} -> {prod}'
                steps.append(step)
                stack.pop()
                symbols = prod.strip().split()
                if symbols != [EPSILON]:
                    for sym in reversed(symbols):
                        stack.append(sym)
            else:
                error = f"No rule for ({top}, {current})"
                step['action'] = f'ERROR: {error}'
                steps.append(step)
                break
        else:
            error = f"Unexpected terminal '{top}' on stack, input '{current}'"
            step['action'] = f'ERROR: {error}'
            steps.append(step)
            break

    return {
        'accepted': error is None and steps[-1]['action'] == 'ACCEPT',
        'steps': steps,
        'error': error
    }
