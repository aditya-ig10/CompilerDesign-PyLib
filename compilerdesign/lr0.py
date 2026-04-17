"""
LR(0) Item Set Construction (Canonical Collection).
"""

from ._utils import EPSILON, stringify_symbols


def _augment(productions: list, start: str) -> tuple:
    aug_start = start + "'"
    aug_prod = [(aug_start, [start])] + list(productions)
    return aug_prod, aug_start


def _closure(items: frozenset, productions: list) -> frozenset:
    closure = set(items)
    changed = True
    while changed:
        changed = False
        for (_, _, after) in list(closure):
            if not after:
                continue
            next_sym = after[0]
            for (plhs, prhs) in productions:
                if plhs == next_sym:
                    new_item = (plhs, (), tuple(prhs))
                    if new_item not in closure:
                        closure.add(new_item)
                        changed = True
    return frozenset(closure)


def _goto(items: frozenset, symbol: str, productions: list) -> frozenset:
    moved = set()
    for (lhs, before, after) in items:
        if after and after[0] == symbol:
            moved.add((lhs, before + (after[0],), after[1:]))
    return _closure(frozenset(moved), productions)


def compute_lr0_items(productions: list, start: str) -> dict:
    """
    Compute the canonical collection of LR(0) item sets.
    """
    aug_prods, aug_start = _augment(productions, start)

    initial_item = (aug_start, (), tuple([start]))
    I0 = _closure(frozenset([initial_item]), aug_prods)

    states = [I0]
    state_map = {I0: 0}
    transitions = []
    queue = [I0]

    while queue:
        current = queue.pop(0)
        current_idx = state_map[current]

        symbols = set()
        for (_, _, after) in current:
            if after:
                symbols.add(after[0])

        for sym in symbols:
            goto = _goto(current, sym, aug_prods)
            if not goto:
                continue
            if goto not in state_map:
                state_map[goto] = len(states)
                states.append(goto)
                queue.append(goto)
            transitions.append((current_idx, sym, state_map[goto]))

    def fmt_item(item):
        lhs, before, after = item
        before_display = stringify_symbols(before)
        after_display = stringify_symbols(after)
        if before_display == EPSILON:
            before_display = ""
        if after_display == EPSILON:
            after_display = ""
        return f"{lhs} -> {before_display} . {after_display}".strip()

    sorted_transitions = sorted(transitions)

    return {
        'states': [
            {
                'id': i,
                'items': sorted([fmt_item(item) for item in state])
            }
            for i, state in enumerate(states)
        ],
        'transitions': sorted_transitions,
        'transition_table': [
            {
                'from_state': from_state,
                'symbol': symbol,
                'to_state': to_state,
            }
            for from_state, symbol, to_state in sorted_transitions
        ],
        'start_state': 0,
        'augmented_start': aug_start,
        'num_states': len(states)
    }
