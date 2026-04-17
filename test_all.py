"""Tests for the compilerdesign library."""
import sys
sys.path.insert(0, '.')

import compilerdesign as cd


def test_help():
    message = cd.help()
    assert "compilerdesign v1.0.1" in message
    assert "Aditya" in message
    assert "aditya-ig10" in message
    print("✓ help")

def test_lexical():
    code = "int main() { int x = 10; return x + 1; }"
    r = cd.lexical_analyzer(code)
    assert r['summary']['keywords'] >= 2
    assert 'x' in r['unique_identifiers']
    print("✓ lexical_analyzer")

def test_left_recursion():
    grammar = {'E': ['E + T', 'T'], 'T': ['T * F', 'F'], 'F': ['( E )', 'id']}
    new_g = cd.eliminate_left_recursion(grammar)
    assert "E'" in new_g
    assert "T'" in new_g
    print("✓ eliminate_left_recursion")

def test_left_factoring():
    grammar = {'A': ['a b', 'a c', 'd']}
    new_g = cd.left_factoring(grammar)
    assert "A'" in new_g
    print("✓ left_factoring")

def test_ambiguity():
    grammar = {'A': ['a', 'a']}  # duplicate
    r = cd.check_ambiguity(grammar)
    assert r['ambiguous'] is True
    print("✓ check_ambiguity")

def test_first_follow():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.compute_first_follow(grammar, start='E')
    assert '(' in r['FIRST']['E']
    assert '$' in r['FOLLOW']['E']
    print("✓ compute_first_follow")

def test_ll1_table():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.build_ll1_table(grammar, start='E')
    assert r['is_ll1'] is True
    print("✓ build_ll1_table")

def test_ll1_parse():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.ll1_parse(grammar, ['i', '+', 'i'], start='E')
    assert r['accepted'] is True
    print("✓ ll1_parse")

def test_shift_reduce():
    productions = [('E', ['E', '+', 'T']), ('E', ['T']), ('T', ['id'])]
    r = cd.shift_reduce_parse(productions, ['id', '+', 'id'])
    assert r['accepted'] is True
    print("✓ shift_reduce_parse")

def test_leading_trailing():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.compute_leading_trailing(grammar)
    assert 'i' in r['LEADING']['E']
    print("✓ compute_leading_trailing")

def test_lr0():
    productions = [('E', ['E', '+', 'T']), ('E', ['T']), ('T', ['id'])]
    r = cd.compute_lr0_items(productions, start='E')
    assert r['num_states'] > 0
    print("✓ compute_lr0_items")

def test_intermediate_code():
    assert cd.infix_to_postfix("a + b * c") == "a b c * +"
    assert cd.infix_to_prefix("a + b * c") == "+ a * b c"
    assert cd.postfix_to_infix("a b c * +") == "(a + (b * c))"
    assert cd.prefix_to_infix("+ a * b c") == "(a + (b * c))"
    assert cd.convert_expression("a + b * c", "infix", "postfix") == "a b c * +"
    print("✓ intermediate_code (all conversions)")

if __name__ == "__main__":
    print("Running compilerdesign tests...\n")
    test_help()
    test_lexical()
    test_left_recursion()
    test_left_factoring()
    test_ambiguity()
    test_first_follow()
    test_ll1_table()
    test_ll1_parse()
    test_shift_reduce()
    test_leading_trailing()
    test_lr0()
    test_intermediate_code()
    print("\n✅ All tests passed!")
