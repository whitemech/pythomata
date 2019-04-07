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

        assert simulator.accepts(["a", "b"])

    def test_raise_exception_when_step_with_unknown_symbol(self):
        """Test that we raise an exception when we try to progress the simulator with a symbol that does not belong
        to the alphabet of the DFA."""

        dfa = DFA(
            {"q0"},
            {"a"},
            "q0",
            {"q0"},
            {}
        )

        simulator = DFASimulator(dfa)

        with pytest.raises(ValueError, match="Symbol 'b' not in the alphabet of the DFA."):
            simulator.step("b")


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
