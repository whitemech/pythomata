# History

## 0.1.0 (2019-04-13)

* Basic support for DFAs and NFAs.
* Algorithms for DFA minimization and trimming.
* Algorithm for NFA determinization.

## 0.2.0 (2019-09-30)

* Refactoring of the repository

## 0.3.0 (2020-02-09)

* Main refactoring of the APIs.
* Introduce interfaces for better abstractions: `Alphabet`, `FiniteAutomaton` etc.
* `DFA` and `NFA` renamed `SimpleDFA` and `SimpleNFA`, respectively.
* Introduced `SymbolicAutomaton` and `SymbolicDFA`, where the guards
  on transitions are propositoinal formulas.
