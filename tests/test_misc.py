# -*- coding: utf-8 -*-
import pytest

from pythomata.base import Sink
from pythomata.dfa import DFA
from pythomata.simulator import DFASimulator


class TestDFASimulator:

    def test_simulator(self):
        dfa = DFA(
            {"q0", "q1", "q2"},
            {"a", "b"},
            "q0",
            {"q2"},
            {
                "q0": {
                    "a": "q1"
                },
                "q1": {
                    "b": "q2"
                },
            }
        )

        simulator = DFASimulator(dfa)

        assert not simulator.is_true()

        simulator.step("a")
        assert not simulator.is_true()
        simulator.step("b")
        assert simulator.is_true()

        simulator.reset()
        assert not simulator.is_true()

        assert simulator.dfa.accepts(["a", "b"])


class TestSink:

    def test_instantiate_sink(self):

        sink1 = Sink()
        sink2 = Sink()

        assert str(sink1) == "sink"
        assert str(sink2) == "sink"

        assert sink1 == sink2
        assert hash(sink1) == hash(sink2)

        s = {sink1, sink2}
        assert len(s) == 1
