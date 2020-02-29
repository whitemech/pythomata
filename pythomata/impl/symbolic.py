# -*- coding: utf-8 -*-
"""
An implementation of a symbolic automaton.

For further details, see:
- Applications of Symbolic Finite Automata
  https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ciaa13.pdf
- Symbolic Automata Constraint Solving
  https://link.springer.com/chapter/10.1007%2F978-3-642-16242-8_45
- Rex: Symbolic Regular Expression Explorer
  https://www.microsoft.com/en-us/research/wp-content/uploads/2010/04/rex-ICST.pdf
"""
import itertools
import operator
from typing import Set, Dict, Union, Any, Optional, FrozenSet, Tuple, AbstractSet

import sympy
from sympy import Symbol, simplify, satisfiable, And, Not, Or
from sympy.logic.boolalg import BooleanFunction, BooleanTrue, BooleanFalse
from sympy.parsing.sympy_parser import parse_expr

from pythomata._internal_utils import greatest_fixpoint
from pythomata.core import FiniteAutomaton, SymbolType, Rendering, DFA, TransitionType
from pythomata.utils import iter_powerset

PropositionalInterpretation = Dict[Union[str, Symbol], bool]


class SymbolicAutomaton(
    Rendering[int, PropositionalInterpretation, BooleanFunction],
    FiniteAutomaton[int, PropositionalInterpretation, BooleanFunction],
):
    """
    A symbolic non-deterministic finite automaton.

    It can recognize sequences of propositional interpretations. E.g.:
    >>> word = [{"a": True, "b": False}, {}]

    If a symbol is not present, it is assumed to be false.

    States are represented as integers. The guards are sympy.BooleanFunction instances.
    """

    def __init__(self):
        """Initialize a Symbolic automaton."""
        super().__init__()
        self._initial_state = 0
        self._states = {0}
        self._final_states = set()  # type: Set[int]
        self._state_counter = 1

        self._transition_function = {}  # type: Dict[int, Dict[int, BooleanFunction]]

    @property
    def states(self) -> Set[int]:
        """Get the states."""
        return self._states

    @property
    def accepting_states(self) -> Set[int]:
        """Get the final states."""
        return self._final_states

    @property
    def initial_state(self) -> int:
        """Get the initial state."""
        return self._initial_state

    def get_successors(
        self, state: int, symbol: PropositionalInterpretation
    ) -> Set[int]:
        """Get the successor states.."""
        if state not in self.states:
            raise ValueError("State not in set of states.")
        if not self._is_valid_symbol(symbol):
            raise ValueError("Symbol {} is not valid.".format(symbol))
        successors = set()
        transition_iterator = self._transition_function.get(state, {}).items()
        for successor, guard in transition_iterator:
            subexpr = guard.subs(symbol)
            subexpr = subexpr.replace(sympy.Symbol, BooleanFalse)
            if subexpr == True:  # noqa: E712
                successors.add(successor)
        return successors

    def create_state(self) -> int:
        """Create a new state."""
        new_state = self._state_counter
        self.states.add(new_state)
        self._state_counter += 1
        return new_state

    def remove_state(self, state: int) -> None:
        """Remove a state."""
        if state not in self.states:
            raise ValueError("State {} not found.".format(state))
        if state == self.initial_state:
            raise ValueError("Cannot remove initial state.")

        self._transition_function.pop(state, None)
        for s in self._transition_function:
            self._transition_function[s].pop(state, None)

        self._states.remove(state)
        if state in self.accepting_states:
            self._final_states.remove(state)

    def set_accepting_state(self, state: int, is_accepting: bool) -> None:
        """Set a state to be final."""
        if state not in self.states:
            raise ValueError("State {} not found.".format(state))
        if is_accepting:
            self.accepting_states.add(state)
        else:
            try:
                self.accepting_states.remove(state)
            except KeyError:
                pass

    def set_initial_state(self, state: int) -> None:
        """Set a state to be an initial state."""
        if state not in self.states:
            raise ValueError("State {} not found.".format(state))
        self._initial_state = state

    def add_transition(
        self, transition: Tuple[int, Union[BooleanFunction, str], int]
    ) -> None:
        """
        Add a transition, i.e. a tuple (source, guard, destination).

        :param transition: the transition to add.
        :return: None
        :raise ValueError: if the source state does not exist.
        :raise ValueError: if the dest state does not exist.
        """
        state1, guard, state2 = transition
        assert state1 in self.states
        assert state2 in self.states
        if isinstance(guard, str):
            guard = simplify(parse_expr(guard))
        other_guard = self._transition_function.get(state1, {}).get(state2, None)
        if other_guard is None:
            self._transition_function.setdefault(state1, {})[state2] = simplify(guard)
        else:
            # take the OR of the two guards.
            self._transition_function[state1][state2] = simplify(other_guard | guard)

    def _is_valid_symbol(self, symbol: Any) -> bool:
        """Return true if the given symbol is valid, false otherwise."""
        try:
            assert isinstance(symbol, dict)
            assert all(isinstance(k, str) for k in symbol.keys())
            assert all(isinstance(v, bool) for v in symbol.values())
        except AssertionError:
            return False
        return True

    def complete(self) -> "SymbolicAutomaton":
        """Complete the automaton."""
        states = set(self.states)
        initial_state = self.initial_state
        final_states = self.accepting_states
        transitions = set()
        sink_state = None
        for source in states:
            transitions_from_source = self._transition_function.get(source, {})
            transitions.update(
                set(
                    map(lambda x: (source, x[1], x[0]), transitions_from_source.items())
                )
            )
            guards = transitions_from_source.values()
            guards_negation = simplify(Not(Or(*guards)))
            if satisfiable(guards_negation) is not False:
                sink_state = len(states) if sink_state is None else sink_state
                transitions.add((source, guards_negation, sink_state))

        if sink_state is not None:
            states.add(sink_state)
            transitions.add((sink_state, BooleanTrue(), sink_state))
        return SymbolicAutomaton._from_transitions(
            states, initial_state, final_states, transitions
        )

    def is_complete(self) -> bool:
        """
        Check whether the automaton is complete.

        :return: True if the automaton is complete, False otherwise.
        """
        # all the state must have an outgoing transition.
        if not all(state in self._transition_function.keys() for state in self.states):
            return False

        for source in self._transition_function:
            guards = self._transition_function[source].values()
            negated_guards = Not(Or(*guards))
            if satisfiable(negated_guards):
                return False

        return True

    def determinize(self) -> "SymbolicDFA":
        """Do determinize."""
        macro_initial_state = frozenset([self._initial_state])  # type: FrozenSet[int]
        stack = [macro_initial_state]
        visited = {macro_initial_state}
        macro_accepting_states = (
            {macro_initial_state}
            if macro_initial_state.intersection(self.accepting_states) != set()
            else set()
        )  # type: Set[FrozenSet[int]]
        moves = set()

        # given an iterable of transitions (i.e. triples (source, guard, destination)),
        # get the guard
        def getguard(x):
            return map(operator.itemgetter(1), x)

        # given ... (as before)
        # get the target
        def gettarget(x):
            return map(operator.itemgetter(2), x)

        while len(stack) > 0:
            macro_source = stack.pop()
            transitions = set(
                [
                    (source, guard, dest)
                    for source in macro_source
                    for dest, guard in self._transition_function.get(source, {}).items()
                ]
            )
            for transitions_subset in map(frozenset, iter_powerset(transitions)):
                if len(transitions_subset) == 0:
                    continue
                transitions_subset_negated = transitions.difference(transitions_subset)
                phi_positive = And(*getguard(transitions_subset))
                phi_negative = And(*map(Not, getguard(transitions_subset_negated)))
                phi = phi_positive & phi_negative
                if sympy.satisfiable(phi) is not False:
                    macro_dest = frozenset(
                        gettarget(transitions_subset)
                    )  # type: FrozenSet[int]
                    moves.add((macro_source, phi, macro_dest))
                    if macro_dest not in visited:
                        visited.add(macro_dest)
                        stack.append(macro_dest)
                        if macro_dest.intersection(self.accepting_states) != set():
                            macro_accepting_states.add(macro_dest)

        return self._from_transitions(
            visited, macro_initial_state, set(macro_accepting_states), moves
        )

    def minimize(self) -> "SymbolicDFA":
        """Minimize the NFA."""
        dfa = self.determinize().complete()
        equivalence_relation = set.union(
            {(p, q) for p, q in itertools.product(dfa.accepting_states, repeat=2)},
            {
                (p, q)
                for p, q in itertools.product(
                    dfa.states.difference(dfa.accepting_states), repeat=2
                )
            },
        )

        def greatest_fixpoint_condition(el: Tuple[int, int], current_set: Set):
            """Condition to say whether the pair must be removed from the bisimulation relation."""
            # unpack the two states
            s_source, t_source = el
            for (s_dest, s_guard) in dfa._transition_function.get(s_source, {}).items():
                for (t_dest, t_guard) in dfa._transition_function.get(
                    t_source, {}
                ).items():
                    if (
                        t_dest != s_dest
                        and (s_dest, t_dest) not in current_set
                        and satisfiable(And(s_guard, t_guard)) is not False
                    ):
                        return True

        # TODO to improve.
        result = greatest_fixpoint(
            equivalence_relation, condition=greatest_fixpoint_condition
        )
        _state2class = {}  # type: Dict[int, Set[int]]
        for a, b in result:
            union = _state2class.get(a, {a}).union(_state2class.get(b, {b}))
            for element in union:
                _state2class[element] = union

        state2class = {
            k: frozenset(v) for k, v in _state2class.items()
        }  # type: Dict[int, FrozenSet[int]]
        equivalence_classes = set(map(lambda x: frozenset(x), state2class.values()))
        class2newstate = dict((ec, i) for i, ec in enumerate(equivalence_classes))

        new_states = set(class2newstate.values())
        old_initial_state = dfa.initial_state
        initial_state = class2newstate[state2class[old_initial_state]]
        final_states = {
            class2newstate[state2class[final_state]]
            for final_state in dfa.accepting_states
        }

        # normalize transitions
        from_edge_to_guard = {}  # type: Dict[Tuple[int, int], BooleanFunction]
        for old_source in dfa._transition_function:
            for old_dest, guard in dfa._transition_function[old_source].items():
                new_source = class2newstate[state2class[old_source]]
                new_dest = class2newstate[state2class[old_dest]]

                edge = (new_source, new_dest)
                if edge in from_edge_to_guard:
                    old_guard = from_edge_to_guard[edge]
                    new_guard = (guard | old_guard).simplify()
                else:
                    new_guard = guard
                from_edge_to_guard[(new_source, new_dest)] = new_guard

        return SymbolicAutomaton._from_transitions(
            new_states,
            initial_state,
            final_states,
            {(u, guard, v) for ((u, v), guard) in from_edge_to_guard.items()},
        )

    @classmethod
    def _from_transitions(
        cls,
        states: Set[Any],
        initial_state: Any,
        final_states: Set[Any],
        transitions: Set[Tuple[Any, SymbolType, Any]],
    ):
        assert initial_state in states
        automaton = SymbolicDFA()
        state_to_indices = {}
        indices_to_state = {}

        initial_state_idx = automaton.initial_state
        state_to_indices[initial_state] = initial_state_idx

        for s in states:
            if s == initial_state:
                automaton.set_accepting_state(initial_state_idx, s in final_states)
                continue
            new_index = automaton.create_state()
            automaton.set_accepting_state(new_index, s in final_states)
            state_to_indices[s] = new_index
            indices_to_state[new_index] = s

        for (source, guard, destination) in transitions:
            source_index = state_to_indices[source]
            dest_index = state_to_indices[destination]
            automaton.add_transition((source_index, guard, dest_index))

        return automaton

    def get_transitions_from(
        self, state: int
    ) -> AbstractSet[Tuple[int, BooleanFunction, int]]:
        """
        Get the outgoing transitions from a state.

        :param state: the starting state.
        :return: the set of transitions object associated with that triple.
                 None if it is not possible to compute such set.
        :raises ValueError: if the state does not belong to the automaton.
        """
        if state not in self.states:
            raise ValueError("The state does not belong to the automaton.")

        transitions = set()
        for end, guard in self._transition_function.get(state, {}).items():
            transitions.add((state, guard, end))

        return transitions


class SymbolicDFA(SymbolicAutomaton, DFA):
    """Implement a symbolic Deterministic Finite Automaton."""

    def set_initial_state(self, state: int) -> None:
        """Set a state to be an initial state."""
        if state not in self.states:
            raise ValueError("State {} not found.".format(state))
        self._initial_state = state

    def add_transition(self, transition: TransitionType) -> None:
        """
        Add a transition, i.e. a tuple (source, guard, destination).

        :param transition: the transition to add.
        :return: None
        :raise ValueError: if the source state does not exist.
        :raise ValueError: if the dest state does not exist.
        """
        state1, guard, state2 = transition
        assert state1 in self.states
        assert state2 in self.states
        if isinstance(guard, str):
            guard = simplify(parse_expr(guard))
        other_guard = self._transition_function.get(state1, {}).get(state2, None)
        if other_guard is None:
            super().add_transition((state1, guard, state2))
        else:
            outgoing_guards = self._transition_function.get(state1, {}).values()
            ors = sympy.Or(*outgoing_guards)
            all_outgoing_guards = sympy.And(ors, guard)
            if sympy.satisfiable(all_outgoing_guards) is False:
                super().add_transition((state1, guard, state2))
            else:
                raise ValueError("Transition is not deterministic.")

    def get_successor(
        self, state: int, symbol: PropositionalInterpretation
    ) -> Optional[int]:
        """
        Get the (unique) successor.

        If not defined, return None.
        """
        successors = super().get_successors(state, symbol)
        assert len(successors) < 2, "Transition must be deterministic"
        return next(iter(successors)) if len(successors) == 1 else None
