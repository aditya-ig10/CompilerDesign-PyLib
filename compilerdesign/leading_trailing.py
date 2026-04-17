"""
Computation of LEADING and TRAILING sets for operator precedence parsing.
"""

from ._utils import EPSILON, normalize_grammar


def compute_leading(grammar: dict) -> dict:
    """
    Compute LEADING sets for all non-terminals.
    """
    grammar = normalize_grammar(grammar)
    leading = {nt: set() for nt in grammar}
    changed = True

    while changed:
        changed = False
        for A, productions in grammar.items():
            for prod in productions:
                symbols = prod.strip().split()
                if not symbols or symbols == [EPSILON]:
                    continue

                i = 0
                while i < len(symbols):
                    sym = symbols[i]
                    if sym not in grammar:
                        before = len(leading[A])
                        leading[A].add(sym)
                        if len(leading[A]) > before:
                            changed = True
                        break
                    else:
                        before = len(leading[A])
                        leading[A].update(leading[sym])
                        if len(leading[A]) > before:
                            changed = True
                        if any(p.strip() == EPSILON for p in grammar[sym]):
                            i += 1
                        else:
                            break

    return {k: sorted(v) for k, v in leading.items()}


def compute_trailing(grammar: dict) -> dict:
    """
    Compute TRAILING sets for all non-terminals.
    """
    grammar = normalize_grammar(grammar)
    trailing = {nt: set() for nt in grammar}
    changed = True

    while changed:
        changed = False
        for A, productions in grammar.items():
            for prod in productions:
                symbols = prod.strip().split()
                if not symbols or symbols == [EPSILON]:
                    continue

                i = len(symbols) - 1
                while i >= 0:
                    sym = symbols[i]
                    if sym not in grammar:
                        before = len(trailing[A])
                        trailing[A].add(sym)
                        if len(trailing[A]) > before:
                            changed = True
                        break
                    else:
                        before = len(trailing[A])
                        trailing[A].update(trailing[sym])
                        if len(trailing[A]) > before:
                            changed = True
                        if any(p.strip() == EPSILON for p in grammar[sym]):
                            i -= 1
                        else:
                            break

    return {k: sorted(v) for k, v in trailing.items()}


def compute_leading_trailing(grammar: dict) -> dict:
    """
    Convenience: returns both LEADING and TRAILING sets.
    """
    return {
        'LEADING': compute_leading(grammar),
        'TRAILING': compute_trailing(grammar)
    }
