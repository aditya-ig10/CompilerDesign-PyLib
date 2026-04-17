"""Internal helpers for producing deterministic, readable outputs."""

EPSILON = "ε"


def sorted_unique(values):
    """Return a deterministic sorted list of unique values."""
    return sorted(set(values))


def normalize_production(production: str) -> str:
    """Normalize epsilon aliases and excess whitespace in a production."""
    cleaned = production.strip().replace("eps", EPSILON)
    if cleaned == EPSILON:
        return EPSILON
    symbols = cleaned.split()
    return " ".join(symbols) if symbols else EPSILON


def normalize_grammar(grammar: dict) -> dict:
    """Normalize every production in a grammar while preserving key order."""
    return {
        non_terminal: [normalize_production(prod) for prod in productions]
        for non_terminal, productions in grammar.items()
    }


def stringify_symbols(symbols) -> str:
    """Render a symbol sequence for display in traces."""
    return " ".join(symbols) if symbols else EPSILON
