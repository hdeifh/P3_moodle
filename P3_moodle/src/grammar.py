from __future__ import annotations

from collections import deque
from typing import Set, AbstractSet, Collection, MutableSet, Optional, Dict, List, Optional

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Grammar:
    """
    Class that represents a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Dictionary with the production rules for each non terminal
          symbol of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        if non_terminals != set(productions.keys()):
            raise ValueError(
                f"Set of non-terminals and productions keys should be equal."
            )
        
        for nt, rhs in productions.items():
            if not rhs:
                raise ValueError(
                    f"No production rules for non terminal symbol {nt} "
                )
            for r in rhs:
                for s in r:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom
        self.first_cache: Dict[str, Set[str]] = {}
        self.follow_cache: Dict[str, Set[str]] = {nt: set() for nt in self.non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )



    def compute_first(self, sentence: List[str]) -> AbstractSet[str]:
        """
        Method to compute the FIRST set of a string.

        Args:
            sentence: list of symbols whose FIRST set is to be computed.

        Returns:
            Set of terminals and/or ε representing FIRST(sentence)
        """

        def _first(seq: List[str]) -> Set[str]:
            first_set: Set[str] = set()

            if not seq:
                first_set.add('')
                return first_set

            for i, symbol in enumerate(seq):
                if symbol in self.terminals:
                    first_set.add(symbol)
                    break  # terminal stops the sequence
                elif symbol in self.non_terminals:
                    # use self.first_cache instead of local cache
                    if symbol not in self.first_cache:
                        self.first_cache[symbol] = set()
                        for production in self.productions[symbol]:
                            self.first_cache[symbol].update(_first(production))

                    first_set.update(self.first_cache[symbol] - {''})

                    if '' not in self.first_cache[symbol]:
                        break  # stop if symbol is not nullable
                else:
                    raise ValueError(f"Symbol {symbol} is neither terminal nor non-terminal.")

                # if last symbol is nullable, add ε
                if i == len(seq) - 1:
                    first_set.add('')

            return first_set

        return _first(sentence)
	# TO-DO: Complete this method for exercise 3...


    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        # Ensure FIRST sets are computed
        for nt in self.non_terminals:
            self.compute_first([nt])

        if symbol not in self.non_terminals:
            raise ValueError(f"{symbol} is not a non-terminal")

        # Initialize FOLLOW cache if it doesn't exist
        self.follow_cache = {nt: set() for nt in self.non_terminals}
        self.follow_cache[self.axiom].add('$')  # Add $ to start symbol

        changed = True
        while changed:
            changed = False
            
            # Iterate over all productions
            for head, productions in self.productions.items():
                for prod in productions:  
                    for i, A in enumerate(prod):
                        if A not in self.non_terminals:
                            continue
                        
                        # ω are the symbols after A
                        omega = prod[i + 1:]
                        
                        # Compute FIRST*(ω)
                        first_omega = set()
                        if omega:
                            for sym in omega:
                                if sym in self.non_terminals:
                                    first_omega |= self.first_cache[sym] - {''}
                                    if '' not in self.first_cache[sym]:
                                        break
                                else:
                                    first_omega.add(sym)
                                    break  
                            else:
                                first_omega.add('')
                        else:
                            first_omega.add('')
                        
                        # FOLLOW(A) += FIRST*(ω) - {ε}
                        to_add = first_omega - {''}
                        if not to_add.issubset(self.follow_cache[A]):
                            self.follow_cache[A] |= to_add
                            changed = True
                        
                        # If ε ∈ FIRST*(ω), FOLLOW(A) += FOLLOW(head)
                        if '' in first_omega:
                            if not self.follow_cache[head].issubset(self.follow_cache[A]):
                                self.follow_cache[A] |= self.follow_cache[head]
                                changed = True

        return self.follow_cache[symbol]
	# TO-DO: Complete this method for exercise 4...


    def get_ll1_table(self) -> Optional[LL1Table]:
        # Ensure FOLLOW sets are computed
        for nt in self.non_terminals:
            self.compute_follow(nt)

        # Terminals = all symbols appearing in productions minus non-terminals
        terminals = set()
        for prods in self.productions.values():
            for prod in prods:
                terminals.update(prod)
        terminals -= self.non_terminals
        terminals.add('$')  # add end-of-input marker

        table = LL1Table(self.non_terminals, terminals)

        for head, prods in self.productions.items():
            for prod in prods:
                # Compute FIRST*(prod)
                first_alpha = self.compute_first(prod)  # returns set including '' if nullable

                # For each terminal in FIRST*(prod) excluding ε
                for terminal in first_alpha - {''}:
                    try:
                        table.add_cell(head, terminal, ''.join(prod))
                    except RepeatedCellError:
                        # Conflict: grammar is not LL(1)
                        return None

                # If ε ∈ FIRST*(prod), add production to FOLLOW(head)
                if '' in first_alpha:
                    for terminal in self.follow_cache[head]:
                        try:
                            table.add_cell(head, terminal, ''.join(prod))
                        except RepeatedCellError:
                            # Conflict: grammar is not LL(1)
                            return None

        return table


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None


class LL1Table:
    """
    LL1 table. Initially all cells are set to None (empty). Table cells
    must be filled by calling the method add_cell.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        self.terminals: AbstractSet[str] = terminals
        self.non_terminals: AbstractSet[str] = non_terminals
        self.cells: Dict[str, Dict[str, Optional[str]]] = {nt: {t: None for t in terminals} for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, non_terminal: str, terminal: str, cell_body: str) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            non_terminal: Non termial symbol (row)
            terminal: Terminal symbol (column)
            cell_body: content of the cell 

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(
                "Trying to add cell for non terminal symbol not included "
                "in table.",
            )
        if terminal not in self.terminals:
            raise ValueError(
                "Trying to add cell for terminal symbol not included "
                "in table.",
            )
        if not all(x in self.terminals | self.non_terminals for x in cell_body):
            raise ValueError(
                "Trying to add cell whose body contains elements that are "
                "not either terminals nor non terminals.",
            )            
        if self.cells[non_terminal][terminal] is not None:
            raise RepeatedCellError(
                f"Repeated cell ({non_terminal}, {terminal}).")
        else:
            self.cells[non_terminal][terminal] = cell_body

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Analyze a string using the LL(1) table and build a parse tree.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object representing the parse tree.

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """
        stack: List[str] = ['$', start]  # symbol stack
        input_list: List[str] = list(input_string)  # input with end-marker
        tree_stack: List[ParseTree] = [ParseTree('$'), ParseTree(start)]  # parse tree nodes

        i = 0  # input pointer
        while i < len(input_list):
            if not stack:
                raise SyntaxError("Stack emptied before input fully consumed")

            stackTop = stack[-1]          # peek top of stack
            current_tree = tree_stack.pop()
            currentSymbol = input_list[i]

            # Terminal or end-marker
            if stackTop in self.terminals or stackTop == '$':
                if stackTop == currentSymbol:
                    stack.pop()   # match terminal
                    i += 1        # consume input symbol
                else:
                    raise SyntaxError(f"Unexpected symbol '{currentSymbol}', expected '{stackTop}'")

            # Non-terminal
            elif stackTop in self.non_terminals:
                production = self.cells.get(stackTop, {}).get(currentSymbol)
                if production is None:
                    raise SyntaxError(f"No rule for '{stackTop}' on input '{currentSymbol}'")

                stack.pop()  # pop non-terminal

                if production == '':  # epsilon production
                    current_tree.children = []
                else:
                    children: List[ParseTree] = []
                    # push RHS symbols in reverse order
                    for symbol in reversed(production):
                        stack.append(symbol)
                        child_tree = ParseTree(symbol)
                        tree_stack.append(child_tree)
                        children.insert(0, child_tree)  # maintain left-to-right order
                    current_tree.children = children

                tree_stack.append(current_tree)  # push updated tree node

            else:
                raise SyntaxError(f"Invalid symbol '{stackTop}' on stack")

        # After processing, stack should only contain end-marker
        if stack != []:
            raise SyntaxError("Input not fully consumed")

        # Return root of parse tree
        return tree_stack[0] if tree_stack else ParseTree(start)             
                
	# TO-DO: Complete this method for exercise 2...
    
    
class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
