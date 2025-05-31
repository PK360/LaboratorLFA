import sys, os
from collections import deque

automata = dict()

def load_pda(file: str):
    global automata
    print('[INFO]: Attempting to load PDA from file...')
    automata = dict()
    with open(file, 'r') as f:
        mat = [i.strip() for i in f.readlines()]
        mat = [i if len(i.strip()) > 0 and i.strip()[0] != '#' else '' for i in mat]
        mat = [i[:i.find('#')].strip() if i.find('#') != -1 else i for i in mat]

        keep, inmode = 0, 0
        for line in range(len(mat)):
            if len(mat[line]) == 0:
                continue

            cur_mode = mat[line][1:mat[line].find(']')]
            if cur_mode.upper() in ['STATES', 'ALPHABET', 'RULES', 'STACK_ALPHABET']:
                if inmode == 3:
                    print('[INFO]: Loaded rule list of PDA...')
                inmode = 0

                if cur_mode.upper() == 'RULES':
                    if 'rules' in automata.keys() and inmode == 0:
                        sys.exit(f'[ERROR]: Redeclaration of rules found at line {line + 1};')
                    elif 'rules' not in automata.keys():
                        automata['rules'] = dict()
                    inmode = 3
                    continue
                else:
                    if cur_mode.upper() == 'STATES':
                        if 'states' in automata.keys() and inmode == 0:
                            sys.exit(f'[ERROR]: Redeclaration of states found at line {line + 1};')
                        elif 'states' not in automata.keys():
                            automata['states'] = []

                        inmode = 1

                        ls = mat[line].split(':')
                        ls = ls[1].strip().split(',')
                        ls = [[j.strip() for j in i.split('=')] for i in ls]
                        for elm in ls:  # Extract states
                            if len(elm[0]) == 0:
                                sys.exit(f'[ERROR]: Empty state defined in state list at line {line + 1};')
                            elif elm[0] in automata['states']:
                                sys.exit(f'[ERROR]: State defined twice in state list at line {line + 1};')
                            if len(elm) > 1:
                                if elm[1].upper() == 'S':
                                    if 'start' not in automata.keys():
                                        automata['start'] = []
                                    else:
                                        sys.exit(f'[ERROR]: More than one start state declared at line {line + 1};')
                                    automata['start'].append(elm[0])
                                    automata['states'].append(elm[0])
                                elif elm[1].upper() == 'E':
                                    if 'accept' not in automata.keys():
                                        automata['accept'] = []
                                    automata['accept'].append(elm[0])
                                    automata['states'].append(elm[0])
                                else:
                                    sys.exit(f'[ERROR]: Wrong specific state type (not S or E) in state definition at line {line + 1};')
                            else:
                                automata['states'].append(elm[0])

                        if len(automata['states']) == 0:
                            sys.exit(f'[ERROR]: No states have been defined for the state list declaration at line {line + 1};')
                        elif 'start' not in automata.keys():
                            sys.exit(f'[ERROR]: State list declared at line {line + 1} does not include a start state (add \'=S\' to a state);')
                        elif 'accept' not in automata.keys():
                            sys.exit(f'[ERROR]: State list declared at line {line + 1} does not include accept states (add \'=E\' to a state);')

                        inmode = 0
                        print('[INFO]: Loaded state list of PDA...')
                    elif cur_mode.upper() == 'ALPHABET':
                        if 'alphabet' in automata.keys() and inmode == 0:
                            sys.exit(f'[ERROR]: Redeclaration of alphabet found at line {line + 1};')
                        elif 'alphabet' not in automata.keys():
                            automata['alphabet'] = []

                        inmode = 2

                        ls = mat[line].split(':')
                        ls = ls[1].strip('{} ').split(',')
                        ls = [i.strip() for i in ls]
                        for elm in ls:  # Extract alphabet
                            if len(elm) == 0:
                                sys.exit(f'[ERROR]: Empty symbol defined in alphabet at line {line + 1};')
                            elif elm in automata['alphabet']:
                                sys.exit(f'[ERROR]: Symbol defined twice in alphabet at line {line + 1};')
                            automata['alphabet'].append(elm)

                        if len(automata['alphabet']) == 0:
                            sys.exit(f'[ERROR]: Alphabet declared at line {line + 1} contains no elements;')
                        inmode = 0
                        print('[INFO]: Loaded alphabet set of PDA...')
                    elif cur_mode.upper() == 'STACK_ALPHABET':
                        if 'stack_alphabet' in automata.keys() and inmode == 0:
                            sys.exit(f'[ERROR]: Redeclaration of stack alphabet found at line {line + 1};')
                        elif 'stack_alphabet' not in automata.keys():
                            automata['stack_alphabet'] = []

                        inmode = 4

                        ls = mat[line].split(':')
                        ls = ls[1].strip('{} ').split(',')
                        ls = [i.strip() for i in ls]
                        for elm in ls:  # Extract stack alphabet
                            if len(elm) == 0:
                                sys.exit(f'[ERROR]: Empty symbol defined in stack alphabet at line {line + 1};')
                            elif elm in automata['stack_alphabet']:
                                sys.exit(f'[ERROR]: Symbol defined twice in stack alphabet at line {line + 1};')
                            automata['stack_alphabet'].append(elm)

                        if len(automata['stack_alphabet']) == 0:
                            sys.exit(f'[ERROR]: Stack alphabet declared at line {line + 1} contains no elements;')
                        inmode = 0
                        print('[INFO]: Loaded stack alphabet set of PDA...')
            elif inmode == 3:
                ls = mat[line].split(',')
                ls = [i.strip() for i in ls]

                if len(ls) == 3:
                    in1, in2, in3 = ls
                    in4, in5 = 'eps', 'eps'
                elif len(ls) == 5:
                    in1, in2, in3, in4, in5 = ls
                else:
                    sys.exit(f'[ERROR]: Rule definition does not contain 3 or 5 elements at line {line + 1} (see pda.txt for more details);')

                if in1 not in automata['states']:
                    sys.exit(f'[ERROR]: Start state of rule defined at line {line + 1} ({in1}) is not in the list of states;')
                elif in3 not in automata['states']:
                    sys.exit(f'[ERROR]: End state of rule defined at line {line + 1} ({in3}) is not in the list of states;')
                elif in2 not in automata['alphabet'] and in2 != 'eps':
                    sys.exit(f'[ERROR]: Transition input defined at line {line + 1} ({in2}) is not in alphabet;')
                elif in4 not in automata['stack_alphabet'] and in4 != 'eps':
                    sys.exit(f'[ERROR]: Stack top input defined at line {line + 1} ({in4}) is not in stack alphabet;')
                elif in5 not in automata['stack_alphabet'] and in5 != 'eps':
                    sys.exit(f'[ERROR]: Stack replacement input defined at line {line + 1} ({in5}) is not in stack alphabet;')

                if (in1, in2) not in automata['rules']:
                    automata['rules'][(in1, in2)] = []
                automata['rules'][(in1, in2)].append((in3, in4, in5))
            elif inmode == 0:
                sys.exit(f'[ERROR]: Non-commented text not part of PDA declaration found at line {line + 1};')

        if inmode == 3:
            print('[INFO]: Loaded rule list of PDA...')

        print('[INFO]: Loading PDA from file was successful!\n')


def eps_close(conf) -> set:
    closure = set(conf)
    queue = deque(conf)

    while queue:
        (q, stack) = queue.popleft()
        top_s = stack[-1] if stack else None

        if (q, 'eps') in automata['rules']:
            for (to, pop, push) in automata['rules'][(q, 'eps')]:
                if pop == 'eps' or (len(stack) != 0 and pop == top_s):
                    new_s = list(stack)

                    if pop != 'eps': new_s.pop()
                    if push != 'eps': new_s.append(push)

                    new_l = (to, tuple(new_s))
                    if new_l not in closure:
                        closure.add(new_l)
                        queue.append(new_l)

    return closure


def check_input(inp: str) -> bool:
    global automata
    wrong = []
    for s in range(len(inp)):
        if inp[s] not in automata['alphabet']:
            wrong.append(s)

    if len(wrong) == 0:
        return True
    elif len(wrong) == 1:
        sys.exit(
            f'[ERROR]: Input {inp} contains a symbol at position {wrong[0]} not defined in the alphabet set {{{', '.join(str(i) for i in automata['alphabet'])}}} of the inputted automata;')
    elif len(wrong) > 1:
        sys.exit(
            f'[ERROR]: Input {inp} contains symbols at positions {', '.join(str(i) for i in wrong)} not defined in the alphabet set {{{', '.join(str(i) for i in automata['alphabet'])}}} of the inputted automata;')


def verify_input(inp) -> bool:
    global automata
    check_input(inp)

    conf = eps_close({(automata['start'][0], tuple())})

    for s in inp:
        next_c = set()
        for (q, stack) in conf:
            top_s = stack[-1] if stack else None
            if (q, s) in automata['rules']:
                for (to, pop, push) in automata['rules'][(q, s)]:
                    if pop == 'eps' or (len(stack) != 0 and pop == top_s):
                        new_s = list(stack)

                        if pop != 'eps': new_s.pop()
                        if push != 'eps': new_s.append(push)

                        next_c.add((to, tuple(new_s)))
        conf = eps_close(next_c)
        if not conf:
            print(f'[RESULT]: String \'{inp}\' was not accepted;')
            return False

    conf = eps_close(conf)
    if any(q in set(automata['accept']) for (q, _) in conf):
        print(f'[RESULT]: String \'{inp}\' was accepted;')
        return True
    print(f'[RESULT]: String \'{inp}\' was not accepted;')
    return False


if len(sys.argv) > 1:
    if len(sys.argv) < 3:
        sys.exit('[ERROR]: Two arguments are required: file containing PDA + input string(s);')

    if not os.path.exists(sys.argv[1]):
        sys.exit(f'[ERROR]: Inputted file ({sys.argv[1]}) does not exist in the current directory;')

    print(f'\n[INFO]: Reading PDA from \'{sys.argv[1]}\'...')
    load_pda(sys.argv[1])

    for i in range(2, len(sys.argv)):
        verify_input(sys.argv[i])
else:
    if not os.path.exists('pda.txt'):
        sys.exit(f'[ERROR]: The included test (pda.txt) does not exist in the current directory;')

    print(f'\n[INFO]: Reading PDA from \'pda.txt\'...')
    load_pda('pda.txt')

    verify_input('00001111')
    verify_input('000011111')
    verify_input('0011')
    verify_input('1100')



    if not os.path.exists('pda_1.txt'):
        sys.exit(f'[ERROR]: The included test (pda_1.txt) does not exist in the current directory;')

    print(f'\n[INFO]: Reading PDA from \'pda_1.txt\'...')
    load_pda('pda_1.txt')

    verify_input('11000011')
    verify_input('10101010')
    verify_input('01011010')
    verify_input('11110000')