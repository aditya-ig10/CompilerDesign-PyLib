"""
Grammar transformations: eliminate left recursion and perform left factoring.

Grammar format:
    A dict mapping non-terminal (str) -> list of productions (list of str).
    Each production is a space-separated string of symbols.
    Use 'eps' or 'ε' to represent epsilon.
"""

from ._utils import EPSILON, normalize_grammar, normalize_production
def eliminate_left_recursion(grammar: dict) -> dict:
    """
    Eliminate immediate left recursion from each production.
    Handles A -> A alpha | beta patterns.

    Returns a new grammar dict with left recursion eliminated.
    """
    normalized_grammar = normalize_grammar(grammar)
    new_grammar = {}
    for A, productions in normalized_grammar.items():
        alpha = []
        beta = []

        for prod in productions:
            symbols = prod.split()
            if symbols[0] == A:
                alpha.append(' '.join(symbols[1:]))
            else:
                beta.append(' '.join(symbols))

        if not alpha:
            new_grammar[A] = productions
        else:
            A_prime = A + "'"
            new_grammar[A] = [b + ' ' + A_prime for b in beta] if beta else [A_prime]
            new_grammar[A_prime] = [a + ' ' + A_prime for a in alpha] + [EPSILON]

    return normalize_grammar(new_grammar)


def left_factoring(grammar: dict) -> dict:
    """
    Apply left factoring to eliminate common prefixes in productions.

    Returns a new grammar dict after left factoring.
    """
    normalized_grammar = normalize_grammar(grammar)
    new_grammar = {}
    counter = {}

    def _factor(A, productions):
        if len(productions) <= 1:
            new_grammar[A] = [normalize_production(p) for p in productions]
            return

        groups = {}
        for prod in productions:
            symbols = normalize_production(prod).split()
            first = symbols[0] if symbols else EPSILON
            groups.setdefault(first, []).append(symbols)

        new_prods = []
        for _, group in groups.items():
            if len(group) == 1:
                new_prods.append(' '.join(group[0]))
            else:
                lcp = group[0]
                for g in group[1:]:
                    lcp = _common_prefix(lcp, g)

                counter[A] = counter.get(A, 0) + 1
                A_prime = A + "'" * counter[A]
                new_prods.append(' '.join(lcp) + ' ' + A_prime)

                remainders = []
                for g in group:
                    rest = g[len(lcp):]
                    remainders.append(' '.join(rest) if rest else EPSILON)

                _factor(A_prime, remainders)

        new_grammar[A] = new_prods

    def _common_prefix(a, b):
        prefix = []
        for x, y in zip(a, b):
            if x == y:
                prefix.append(x)
            else:
                break
        return prefix

    for A, productions in normalized_grammar.items():
        _factor(A, productions)

    return normalize_grammar(new_grammar)


def check_ambiguity(grammar: dict) -> dict:
    """
    Basic ambiguity check: detects if any non-terminal has duplicate productions
    or productions with the same first symbol (a heuristic, not complete detection).

    Returns {'ambiguous': bool, 'issues': list of str}
    """
    normalized_grammar = normalize_grammar(grammar)
    issues = []
    for A, prods in normalized_grammar.items():
        norm = [normalize_production(p) for p in prods]
        if len(norm) != len(set(norm)):
            issues.append(f"{A} has duplicate productions.")
        first_symbols = [p.split()[0] if p.split() else EPSILON for p in norm]
        if len(first_symbols) != len(set(first_symbols)):
            issues.append(f"{A} has productions with the same leading symbol (possible ambiguity).")

    return {
        'ambiguous': len(issues) > 0,
        'issue_count': len(issues),
        'issues': sorted(issues)
    }
