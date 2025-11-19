import unittest
from typing import AbstractSet

from src.grammar import Grammar
from src.utils import GrammarFormat


class TestFollow(unittest.TestCase):
    def _check_follow(
        self,
        grammar: Grammar,
        symbol: str,
        follow_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"Follow({symbol}), expected {follow_set}",
        ):
            computed_follow = grammar.compute_follow(symbol)
            self.assertEqual(computed_follow, follow_set)

    def test_case1(self) -> None:
        """FOLLOW for original grammar with nullable X and Y."""
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

        self._check_follow(grammar, "E", {'$', ')'})
        self._check_follow(grammar, "X", {'$', ')'})
        self._check_follow(grammar, "T", {'+', '$', ')'})
        self._check_follow(grammar, "Y", {'+', '$', ')'})
    
    def test_case2_terminals_only(self) -> None:
        """FOLLOW when grammar contains only terminals."""
        grammar_str = """
        S -> aB
        B -> b
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "B", {'$'})

    def test_case3_nullable_sequences(self) -> None:
        """FOLLOW with nullable non-terminals."""
        grammar_str = """
        S -> AB
        A ->
        B -> b
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "A", {'b'})
        self._check_follow(grammar, "B", {'$'})

    def test_case4_multiple_nullable(self) -> None:
        """FOLLOW with multiple consecutive nullable non-terminals."""
        grammar_str = """
        S -> ABC
        A ->
        B ->
        C -> c
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "A", {'c'})
        self._check_follow(grammar, "B", {'c'})
        self._check_follow(grammar, "C", {'$'})

    def test_case5_terminal_and_nonterminal_mix(self) -> None:
        """FOLLOW with mixed terminals and non-terminals."""
        grammar_str = """
        S -> aB
        B -> bC
        C -> c
        C ->
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "B", {'$'})
        self._check_follow(grammar, "C", {'$'})

    def test_case6_empty_string(self) -> None:
        """FOLLOW of a grammar with only empty productions."""
        grammar_str = """
        S -> A
        A ->
        """
        grammar = GrammarFormat.read(grammar_str)
        self._check_follow(grammar, "S", {'$'})
        self._check_follow(grammar, "A", {'$'})


if __name__ == '__main__':
    unittest.main()
