"""FIRST and FOLLOW set computation for context-free grammars."""

from ._utils import EPSILON, normalize_grammar

END_MARKER = '$'


def compute_first(grammar: dict) -> dict:
    """
    Compute FIRST sets for all non-terminals in the grammar.
    """
    grammar = normalize_grammar(grammar)
    first = {nt: set() for nt in grammar}

    def first_of(symbol):
        if symbol not in grammar:
            return {symbol}
        return first[symbol]

    changed = True
    while changed:
        changed = False
        for A, productions in grammar.items():
            for prod in productions:
                symbols = prod.strip().split()
                if not symbols or symbols == [EPSILON]:
                    if EPSILON not in first[A]:
                        first[A].add(EPSILON)
                        changed = True
                    continue

                before = len(first[A])
                for sym in symbols:
                    sym_first = first_of(sym)
                    first[A].update(sym_first - {EPSILON})
                    if EPSILON not in sym_first:
                        break
                else:
                    first[A].add(EPSILON)

                if len(first[A]) > before:
                    changed = True

    return {k: sorted(v) for k, v in first.items()}


def compute_follow(grammar: dict, start: str = None) -> dict:
    """
    Compute FOLLOW sets for all non-terminals in the grammar.
    Requires the start symbol (defaults to the first key in grammar).
    """
    grammar = normalize_grammar(grammar)
    if start is None:
        start = next(iter(grammar))

    first_sets = compute_first(grammar)
    follow = {nt: set() for nt in grammar}
    follow[start].add(END_MARKER)

    def first_of_sequence(symbols):
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

    changed = True
    while changed:
        changed = False
        for A, productions in grammar.items():
            for prod in productions:
                symbols = prod.strip().split()
                if symbols == [EPSILON]:
                    continue
                for i, B in enumerate(symbols):
                    if B not in grammar:
                        continue
                    beta = symbols[i + 1:]
                    before = len(follow[B])
                    if beta:
                        first_beta = first_of_sequence(beta)
                        follow[B].update(first_beta - {EPSILON})
                        if EPSILON in first_beta:
                            follow[B].update(follow[A])
                    else:
                        follow[B].update(follow[A])
                    if len(follow[B]) > before:
                        changed = True

    return {k: sorted(v) for k, v in follow.items()}


def compute_first_follow(grammar: dict, start: str = None) -> dict:
    """
    Convenience function: returns both FIRST and FOLLOW sets.
    """
    return {
        'FIRST': compute_first(grammar),
        'FOLLOW': compute_follow(grammar, start)
    }
