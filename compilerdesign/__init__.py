"""
compilerdesign (cd) - A Python library for demonstrating compiler design concepts.

Usage:
    import compilerdesign as cd

    # Lexical Analysis
    result = cd.lexical_analyzer(source_code)

    # Grammar transformations
    new_grammar = cd.eliminate_left_recursion(grammar)
    new_grammar = cd.left_factoring(grammar)
    result = cd.check_ambiguity(grammar)

    # FIRST and FOLLOW sets
    result = cd.compute_first_follow(grammar, start='E')

    # LL(1) Parsing Table
    table = cd.build_ll1_table(grammar)
    parse_result = cd.ll1_parse(grammar, tokens)

    # Shift-Reduce Parsing
    result = cd.shift_reduce_parse(productions, tokens)

    # LEADING and TRAILING
    result = cd.compute_leading_trailing(grammar)

    # LR(0) Items
    result = cd.compute_lr0_items(productions, start='E')

    # Expression conversion
    postfix = cd.infix_to_postfix("a + b * c")
    prefix  = cd.infix_to_prefix("a + b * c")
    infix   = cd.postfix_to_infix("a b c * +")
    result  = cd.convert_expression("a + b * c", "infix", "postfix")
"""

__version__ = "1.0.1"
__author__ = "Aditya"
__github__ = "aditya-ig10"


def help() -> str:
    """Return a readable overview of the package and its main utilities."""
    message = f"""
compilerdesign v{__version__}

A Python library for learning core compiler design concepts.

Main features:
- Lexical analysis
- Grammar transformations
- FIRST and FOLLOW sets
- LL(1) parsing table construction and parsing
- Shift-reduce parsing
- LEADING and TRAILING sets
- LR(0) item set construction
- Infix, postfix, and prefix expression conversion

Quick usage:
    import compilerdesign as cd
    result = cd.lexical_analyzer("int x = 10;")

Developer:
- Aditya
- GitHub: https://github.com/{__github__}
""".strip()
    print(message)
    return message

from .first_follow import compute_first, compute_first_follow, compute_follow
from .grammar import check_ambiguity, eliminate_left_recursion, left_factoring
from .intermediate_code import (
    convert_expression,
    infix_to_postfix,
    infix_to_prefix,
    postfix_to_infix,
    postfix_to_prefix,
    prefix_to_infix,
    prefix_to_postfix,
)
from .leading_trailing import compute_leading, compute_leading_trailing, compute_trailing
from .lexical import lexical_analyzer
from .ll1 import build_ll1_table, ll1_parse
from .lr0 import compute_lr0_items
from .shift_reduce import shift_reduce_parse

__all__ = [
    "help",
    "lexical_analyzer",
    "eliminate_left_recursion",
    "left_factoring",
    "check_ambiguity",
    "compute_first",
    "compute_follow",
    "compute_first_follow",
    "build_ll1_table",
    "ll1_parse",
    "shift_reduce_parse",
    "compute_leading",
    "compute_trailing",
    "compute_leading_trailing",
    "compute_lr0_items",
    "infix_to_postfix",
    "infix_to_prefix",
    "postfix_to_infix",
    "postfix_to_prefix",
    "prefix_to_infix",
    "prefix_to_postfix",
    "convert_expression",
]
