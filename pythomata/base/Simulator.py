from abc import ABC, abstractmethod
from typing import List, Any

from pythomata.base.DFA import DFA
from pythomata.base.Symbol import Symbol


class Simulator(ABC):

    @abstractmethod
    def make_transition(self, s:Symbol) -> Any:
        raise NotImplementedError

    @abstractmethod
    def is_true(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def word_acceptance(self, word: List[Symbol]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_current_state(self):
        raise NotImplementedError


class DFASimulator(Simulator):
    def __init__(self, dfa:DFA):
        self.dfa = dfa.minimize()
        self.id2state = dict(enumerate(self.dfa.states))
        self.state2id = {v: k for k, v in self.id2state.items()}
        self.cur_state = self.state2id[self.dfa.initial_state]


    def make_transition(self, s:Symbol):
        assert s in self.dfa.alphabet.symbols
        transitions = self.dfa.transition_function[self.id2state[self.cur_state]]

        self.cur_state = self.state2id[transitions[s]]


    def is_true(self):
        return self.id2state[self.cur_state] in self.dfa.accepting_states

    def word_acceptance(self, word: List[Symbol]):
        self.reset()
        for s in word:
            self.make_transition(s)
        return self.is_true()

    def reset(self):
        self.cur_state = self.state2id[self.dfa.initial_state]

    def get_current_state(self):
        return self.cur_state
