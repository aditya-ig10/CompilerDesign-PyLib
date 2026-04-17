"""
Shift-Reduce Parsing (bottom-up).

Grammar format:
    List of (LHS, RHS) tuples where RHS is a list of symbols.
    Example: [('E', ['E', '+', 'T']), ('E', ['T']), ('T', ['id'])]
"""

from ._utils import stringify_symbols


def shift_reduce_parse(productions: list, tokens: list) -> dict:
    """
    Simulate shift-reduce parsing with a simple handle-finding heuristic.
    """
    input_tokens = list(tokens) + ['$']
    stack = ['$']
    idx = 0
    steps = []
    error = None
    max_steps = 500

    def find_handle():
        for lhs, rhs in productions:
            rhs_len = len(rhs)
            if len(stack) >= rhs_len + 1:
                top = stack[-rhs_len:]
                if top == list(rhs):
                    return lhs, rhs
        return None, None

    step_count = 0
    while step_count < max_steps:
        step_count += 1
        lhs, rhs = find_handle()
        current_input = input_tokens[idx:]

        step = {
            'step': len(steps) + 1,
            'stack': list(stack),
            'input': list(current_input),
            'stack_display': stringify_symbols(stack),
            'input_display': stringify_symbols(current_input),
            'action': ''
        }

        if lhs is not None:
            step['action'] = f"Reduce: {lhs} -> {' '.join(rhs)}"
            steps.append(step)
            for _ in rhs:
                stack.pop()
            stack.append(lhs)

            if stack == ['$', productions[0][0]] and input_tokens[idx] == '$':
                steps.append({
                    'step': len(steps) + 1,
                    'stack': list(stack),
                    'input': ['$'],
                    'stack_display': stringify_symbols(stack),
                    'input_display': '$',
                    'action': 'ACCEPT',
                })
                break
        else:
            if idx >= len(input_tokens) or input_tokens[idx] == '$':
                error = f"Parsing error: cannot shift '$', no handle found. Stack: {stack}"
                step['action'] = f'ERROR: {error}'
                steps.append(step)
                break
            token = input_tokens[idx]
            step['action'] = f'Shift: {token}'
            steps.append(step)
            stack.append(token)
            idx += 1
    else:
        error = "Max steps exceeded - possible infinite loop or unrecognized grammar."

    accepted = not error and steps and steps[-1]['action'] == 'ACCEPT'
    return {
        'accepted': accepted,
        'steps': steps,
        'error': error
    }
