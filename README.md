# Laborator LFA
This repository contains all the lab work I have done in this semester for LFA.

There are 4 different Python scripts found in each one of the folders, all of them being my implementations of emulators for automatas.


## 1. DFA (Deterministic Finite Automata)
The *'dfa.py'* script found in the DFA directory takes a formatted text file and builds a DFA in a *dictionary*, which then can run input strings given by the user. If run without any inputs, the script *defaults to processing 2 files found in the same directory* and running their DFAs on some predefined inputs.

Defining *start / accept states* is done by adding *= S* / *= E* after the definition of a state (there can only be one start state at a time).

Files should be formatted like this example:
```
# You can add single-line comments with '#' at the start of a line or after a line

[STATES]: q0 = S, q1 = E
[ALPHABET]: {0, 1}   # alphabet elements have to be declared in curly brackets
[RULES]
q0, 0, q1
q0, 1, q1
q1, 0, q0
q1, 1, q0
```


## 2. NFA (Non-deterministic Finite Automata)
The *'nfa.py'* script found in the NFA directory also processes inputs like the DFA emulator.

However, in terms of emulation, since NFAs introduce *branch splitting* when processing inputs (which is a consequence of their non-determinism), emulating a NFA in an accurate way can be done by making the input processing a *recursion*. At the same time, this recursion also needs to determine all possible current states for a state, which is done using an *ε-closure* (a set of all reachable states from a certain state using only ε transitions).

Going forward, ε is declared in emulators as the predefined symbol *'eps'*, which ***does not need to be included in any alphabet definition***.

Files should be formatted like this example, which uses the same formatting as a DFA:
```
[STATES]: q1 = s, q2, q3, q4 = E
[ALPHABET]: {0, 1}
[RULES]
q1, 0, q1
q1, 1, q1
q1, 1, q2
q2, 0, q3
q2, eps, q3
q3, 1, q4
q4, 0, q4
q4, 1, q4
```

## 3. PDA (Push-Down Automata)
The *'pda.py'* script found in the PDA directory emulates specifically non-deterministic PDAs.

Compared to NFAs, input processing is done in a *non-recursive* way, where the ε-closure of a state is instead defined as a set of all *currently reachable states* from a state with only ε transitions, along with the *modified stack corresponding to each reachable state*.

Files should be formatted like this slightly modified example:
```
[STATES]: q0 = S, q1, q2, q3 = E
[ALPHABET]: {0, 1}
[STACK_ALPHABET]: {0, $}   # stack alphabet elements are also defined in curly brackets
[RULES]
q0, eps, q1, eps, $
q1, 0, q1, eps, 0
q1, 1, q2, 0, eps
q2, 1, q2, 0, eps
q2, eps, q3, $, eps
```

## 4. Turing Machines
The *'turing.py'* script found in the Turing directory processes input similar to the other emulators.

Compared to the usual 7-tuple definition of a Turing Machine, this emulated version *forgoes the tape alphabet*, implementing a form of ε transitions instead that are defined as:
- **ε -> ε:** can be used for moving regardless of the tape input
- **symbol -> ε:** can be used for transitions / movement without modifying the tape input

The empty input of a Turing Machine is also *hard-coded to be SPACE*, which can and will only be introduced in the alphabet of the machine at runtime.

Compared to the other emulators presented above, this emulator adds the special *'reject'* state of Turing Machines, declared by adding *= R* after defining a state.\
Accept / Reject states automatically end the execution of the tape.

Rules are defined in 3 different ways:
1. **3-tuples:** *(start, end, direction)*
   - tape input and output are defaulted to ε;
2. **4-tuples:** *(start, inp, end, direction)* or *(start, end, outp, direction)*
   - tape input becomes equal to the output;
3. **5-tuples:** *(start, inp, end, outp, direction)*
   - this is the full variant of a rule;

Files should be formatted like this example:
```
[STATES]: q0 = S, q1
[ALPHABET]: {1}
[RULES]
q0, ,q1,1,R
q1, ,q0, ,R
q1,q1,R
q0,q0,R
q0,q0,1,R
```

## IMPORTANT!!
A limitation with this implementation is that ***you cannot use #*** as an element of your automata, since it ***will be counted as the start of a comment*** and so the emulator will ignore the rest of the line after it. This is common to all emulators presented above.

