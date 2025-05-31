import sys, os

automata = dict()
check = False

def load_nfa(file: str):
    global automata
    print('[INFO]: Attempting to load NFA from file...')
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
            if cur_mode.upper() in ['STATES', 'ALPHABET', 'RULES']:
                if inmode == 3:
                    print('[INFO]: Loaded rule list of NFA...')
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
                        for elm in ls: # Extract states
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
                        print('[INFO]: Loaded state list of NFA...')
                    elif cur_mode.upper() == 'ALPHABET':
                        if 'alphabet' in automata.keys() and inmode == 0:
                            sys.exit(f'[ERROR]: Redeclaration of alphabet found at line {line + 1};')
                        elif 'alphabet' not in automata.keys():
                            automata['alphabet'] = []

                        inmode = 2

                        ls = mat[line].split(':')
                        ls = ls[1].strip('{} ').split(',')
                        ls = [i.strip() for i in ls]
                        for elm in ls: # Extract alphabet
                            if len(elm) == 0:
                                sys.exit(f'[ERROR]: Empty symbol defined in alphabet at line {line + 1};')
                            elif elm in automata['alphabet']:
                                sys.exit(f'[ERROR]: Symbol defined twice in alphabet at line {line + 1};')
                            automata['alphabet'].append(elm)

                        if len(automata['alphabet']) == 0:
                            sys.exit(f'[ERROR]: Alphabet declared at line {line+ 1} contains no elements;')
                        inmode = 0
                        print('[INFO]: Loaded alphabet set of NFA...')
            elif inmode == 3:
                ls = mat[line].split(',')
                ls = [i.strip() for i in ls]

                if len(ls) != 3:
                    sys.exit(f'[ERROR]: Rule definition does not contain 3 elements (start, input, end) at line {line + 1};')
                elif ls[0] not in automata['states']:
                    sys.exit(f'[ERROR]: Start state of rule defined at line {line + 1} ({ls[0]}) is not in the list of states;')
                elif ls[2] not in automata['states']:
                    sys.exit(f'[ERROR]: End state of rule defined at line {line + 1} ({ls[2]}) is not in the list of states;')
                elif ls[1] not in automata['alphabet'] and ls[1] != 'eps':
                    sys.exit(f'[ERROR]: Transition input defined at line {line + 1} ({ls[1]}) is not in alphabet;')

                if (ls[0], ls[1]) not in automata['rules'].keys():
                    automata['rules'][(ls[0], ls[1])] = []
                automata['rules'][(ls[0], ls[1])].append(ls[2])
            elif inmode == 0:
                sys.exit(f'[ERROR]: Non-commented text not part of NFA declaration found at line {line + 1};')

        if inmode == 3:
            print('[INFO]: Loaded rule list of NFA...')

        print('[INFO]: Loading NFA from file was successful!\n')


def eps_close(state: str) -> list:
    stack = list(state)
    closure = set(stack)

    while stack:
        cur_state = stack.pop()

        if (cur_state, 'eps') in automata['rules'].keys():
            for nxt in automata['rules'][(cur_state, 'eps')]:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)

    return list(closure)


def check_input(inp: str) -> bool:
    global automata
    wrong = []
    for s in range(len(inp)):
        if inp[s] not in automata['alphabet']:
            wrong.append(s)

    if len(wrong) == 0:
        return True
    elif len(wrong) == 1:
        sys.exit(f'[ERROR]: Input {inp} contains a symbol at position {wrong[0]} not defined in the alphabet set {{{', '.join(str(i) for i in automata['alphabet'])}}} of the inputted automata;')
    elif len(wrong) > 1:
        sys.exit(f'[ERROR]: Input {inp} contains symbols at positions {', '.join(str(i) for i in wrong)} not defined in the alphabet set {{{', '.join(str(i) for i in automata['alphabet'])}}} of the inputted automata;')


def recursion(inp: str, cur_state):
    global check
    if len(inp) == 0:
        return cur_state[0] in automata['accept']
    else:
        current = eps_close(cur_state)
        for state in current:
            if check:
                return True

            if (state, inp[0]) in automata['rules'].keys():
                for end in automata['rules'][(state, inp[0])]:
                    check = check or recursion(inp[1:], [end])
            else:
                check = False

    return check


def verify_input(inp) -> bool:
    global check, automata
    check = False
    check_input(inp)

    if recursion(inp, automata['start']):
        print(f'[RESULT]: String \'{inp}\' was accepted;')
        return True
    print(f'[RESULT]: String \'{inp}\' was not accepted;')
    return False



if len(sys.argv) > 1:
    if len(sys.argv) < 3:
        sys.exit('[ERROR]: Two arguments are required: file containing NFA + input string(s);')

    if not os.path.exists(sys.argv[1]):
        sys.exit(f'[ERROR]: Inputted file ({sys.argv[1]}) does not exist in the current directory;')

    print(f'\n[INFO]: Reading NFA from \'{sys.argv[1]}\'...')
    load_nfa(sys.argv[1])

    for i in range(2, len(sys.argv)):
        verify_input(sys.argv[i])
else:
    if not os.path.exists('nfa.txt'):
        sys.exit(f'[ERROR]: The included test (nfa.txt) does not exist in the current directory;')

    print(f'\n[INFO]: Reading NFA from \'nfa.txt\'...')
    load_nfa('nfa.txt')

    verify_input('0011001100')
    verify_input('0011001000')
    verify_input('0011000100')
    verify_input('1111111011')



    if not os.path.exists('nfa_1.txt'):
        sys.exit(f'[ERROR]: The included test (nfa_1.txt) does not exist in the current directory;')

    print(f'\n[INFO]: Reading NFA from \'nfa_1.txt\'...')
    load_nfa('nfa_1.txt')

    verify_input('0011000000')
    verify_input('0010010000')
    verify_input('0010100000')
    verify_input('0000000000')