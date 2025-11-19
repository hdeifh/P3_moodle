import unittest
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})

    def test_case2_terminals_only(self) -> None:
        """Test FIRST on terminal-only sequences."""
        grammar_str = """
        S -> aB
        B -> b
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "a", {'a'})
        self._check_first(grammar, "ab", {'a'})
        self._check_first(grammar, "B", {'b'})

    def test_case3_nullable_sequences(self) -> None:
        """Test FIRST with nullable non-terminals."""
        grammar_str = """
        S -> AB
        A ->
        B -> b
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "S", {'b'})
        self._check_first(grammar, "A", {''})
        self._check_first(grammar, "AB", {'b'})

    def test_case4_multiple_nullable(self) -> None:
        """Test FIRST with multiple consecutive nullable non-terminals."""
        grammar_str = """
        S -> ABC
        A ->
        B ->
        C -> c
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "S", {'c'})
        self._check_first(grammar, "AB", {''})
        self._check_first(grammar, "ABC", {'c'})

    def test_case5_terminal_and_nonterminal_mix(self) -> None:
        """Test FIRST with mixed terminals and non-terminals."""
        grammar_str = """
        S -> aB
        B -> bC
        C -> c
        C ->
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "S", {'a'})
        self._check_first(grammar, "B", {'b'})
        self._check_first(grammar, "C", {'c', ''})
        self._check_first(grammar, "BC", {'b'})
        self._check_first(grammar, "aBC", {'a'})

    def test_case6_empty_string(self) -> None:
        """Test FIRST of empty string."""
        grammar_str = """
        S -> A
        A ->
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "S", {''})
        self._check_first(grammar, "A", {''})

if __name__ == '__main__':
    unittest.main()
