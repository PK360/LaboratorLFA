import sys, os

automata = dict()

def load_turing(file: str):
    global automata
    print('[INFO]: Attempting to load Turing Machine from file...')
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
                    print('[INFO]: Loaded rule list of Turing Machine...')
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
                                        sys.exit(f'[ERROR]: Turing Machine declares more than one start state at line {line + 1};')
                                    automata['start'].append(elm[0])
                                    automata['states'].append(elm[0])
                                elif elm[1].upper() == 'E':
                                    if 'accept' not in automata.keys():
                                        automata['accept'] = []
                                    automata['accept'].append(elm[0])
                                    automata['states'].append(elm[0])
                                elif elm[1].upper() == 'R':
                                    if 'reject' not in automata.keys():
                                        automata['reject'] = []
                                    automata['reject'].append(elm[0])
                                    automata['states'].append(elm[0])
                                else:
                                    sys.exit(f'[ERROR]: Wrong specific state type ({elm[1].upper()}, not S, E or R) in state definition at line {line + 1};')
                            else:
                                automata['states'].append(elm[0])

                        if len(automata['states']) == 0:
                            sys.exit('[ERROR]: No states have been defined;')
                        elif 'start' not in automata.keys():
                            sys.exit('[ERROR]: Turing Machine does not have a start state (add \'=S\' to a state);')

                        if 'accept' not in automata.keys():
                            automata['accept'] = []
                        if 'reject' not in automata.keys():
                            automata['reject'] = []

                        inmode = 0
                        print('[INFO]: Loaded state list of Turing Machine...')
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
                            sys.exit('[ERROR]: Alphabet contains no elements;')

                        automata['alphabet'].append(' ')
                        inmode = 0
                        print('[INFO]: Loaded alphabet set of Turing Machine...')
            elif inmode == 3:
                ls = mat[line].split(',')

                if len(ls) == 4:
                    if ls[2] in automata['alphabet'] or ls[2] == 'eps':
                        in1, in3, in4, in5 = ls
                        in2 = in4
                    elif ls[1] in automata['alphabet'] or ls[1] == 'eps':
                        in1, in2, in3, in5 = ls
                        in4 = in2
                    elif ls[1] not in automata['alphabet'] and ls[1] != 'eps':
                        sys.exit(f'[ERROR]: Transition input defined at line {line + 1} ({ls[1]}) is not in alphabet;')
                    elif ls[2] not in automata['alphabet'] and ls[2] != 'eps':
                        sys.exit(f'[ERROR]: Transition result defined at line {line + 1} ({ls[2]}) is not in alphabet;')

                    if in2 == 'eps' and in4 != 'eps':
                        sys.exit(f'[ERROR]: Epsilon rule defined at line {line + 1} is not correct. They must be of type \'eps\' -> \'eps\' or [symbol] -> \'eps\';')
                elif len(ls) == 5:
                    in1, in2, in3, in4, in5 = ls
                    if in2 == 'eps' and in4 != 'eps':
                        sys.exit(f'[ERROR]: Rule defined at line {line + 1} is not correct. They must be of type \'eps\' -> \'eps\' or [symbol] -> \'eps\';')
                elif len(ls) == 3:
                    in1, in3, in5 = ls
                    in2, in4 = 'eps', 'eps'
                else:
                    sys.exit(f'[ERROR]: Rule definition does not contain 3, 4 or 5 elements at line {line + 1} (see turing_machine.txt for details);')

                if (in1, in2) in automata['rules'].keys():
                    sys.exit(f'[ERROR]: Redefinment of transition for same tuple ({in1}, {in2}) at line {line + 1};')
                elif in1 not in automata['states']:
                    sys.exit(f'[ERROR]: Start state of rule defined at line {line + 1} ({in1}) is not in the list of states;')
                elif in3 not in automata['states']:
                    sys.exit(f'[ERROR]: End state of rule defined at line {line + 1} ({in3}) is not in the list of states;')
                elif in2 not in automata['alphabet'] and in2 != 'eps':
                    sys.exit(f'[ERROR]: Transition input defined at line {line + 1} ({in2}) is not in alphabet;')
                elif in4 not in automata['alphabet'] and in4 != 'eps':
                    sys.exit(f'[ERROR]: Transition result defined at line {line + 1} ({in4}) is not in alphabet;')
                elif in5.lower() not in ['l', 'r']:
                    sys.exit(f'[ERROR]: Direction of rule defined at line {line + 1} ({in5}) is not \'L\' or \'R\';')

                automata['rules'][(in1, in2)] = [in3, in4, in5]
            elif inmode == 0:
                sys.exit(f'[ERROR]: Non-commented text not part of Turing Machine declaration found at line {line + 1};')

        if inmode == 3:
            print('[INFO]: Loaded rule list of Turing Machine...')

        print('[INFO]: Loading Turing Machine from file was successful!\n')


def verify_input(inp) -> bool:
    global automata
    poz, cur_state, orig = 0, automata['start'][0], inp
    should = True

    while should:
        if cur_state in automata['accept']:
            print(f'[RESULT]: The tape ({orig}) reaches ' + ('an' if len(automata['reject']) == 1 else 'the') + f' accept state ({cur_state}), now being: ({inp});')
            return True
        elif cur_state in automata['reject']:
            print(f'[RESULT]: The tape ({orig}) reaches ' + ('a' if len(automata['reject']) == 1 else 'the') + f' reject state ({cur_state}), currently being: ({inp});')
            return False

        tup = (cur_state, inp[poz])
        if tup in automata['rules'].keys():
            if automata['rules'][tup][1] != 'eps':
                inp = inp[:poz] + automata['rules'][tup][1] + inp[poz + 1:]
            if automata['rules'][tup][2] == 'L': poz -= 1
            elif automata['rules'][tup][2] == 'R': poz += 1

            if poz < 0 or poz >= len(inp):
                should = False
                continue
            cur_state = automata['rules'][tup][0]
            continue

        tup = (cur_state, 'eps')
        if tup in automata['rules'].keys():
            if automata['rules'][tup][2] == 'L': poz -= 1
            elif automata['rules'][tup][2] == 'R': poz += 1

            if poz < 0 or poz >= len(inp):
                should = False
                continue
            cur_state = automata['rules'][tup][0]
            continue

        should = False

    if cur_state in automata['accept']:
        print(f'[RESULT]: The tape ({orig}) reaches ' + ('an' if len(automata['reject']) == 1 else 'the') + f' accept state ({cur_state}), now being: ({inp});')
        return True
    elif cur_state in automata['reject']:
        print(f'[RESULT]: The tape ({orig}) reaches ' + ('a' if len(automata['reject']) == 1 else 'the') + f' reject state ({cur_state}), currently being: ({inp});')
        return False
    else:
        print(f'[RESULT]: Reached the end of ({orig}) (current state: {cur_state}), modified to be ({inp});')
        return True



if len(sys.argv) > 1:
    if len(sys.argv) < 3:
        sys.exit('[ERROR]: Two arguments are required: file containing Turing Machine + input string(s);')

    if not os.path.exists(sys.argv[1]):
        sys.exit(f'[ERROR]: Inputted file ({sys.argv[1]}) does not exist in the current directory;')

    print(f'\n[INFO]: Reading Turing Machine from \'{sys.argv[1]}\'...')
    load_turing(sys.argv[1])

    for i in range(2, len(sys.argv)):
        verify_input(sys.argv[i])
else:
    if not os.path.exists('turing_machine.txt'):
        sys.exit(f'[ERROR]: The included test (turing_machine.txt) does not exist in the current directory;')

    print(f'\n[INFO]: Reading Turing Machine from \'turing_machine.txt\'...')
    load_turing('turing_machine.txt')

    verify_input('  1  1  1  1')
    verify_input('            ')
    verify_input(' _____ _____ _____ ')



    if not os.path.exists('turing_machine_1.txt'):
        sys.exit(f'[ERROR]: The included test (turing_machine_1.txt) does not exist in the current directory;')

    print(f'\n[INFO]: Reading Turing Machine from \'turing_machine_1.txt\'...')
    load_turing('turing_machine_1.txt')

    verify_input('110101111011$hsajhahs@            @')
    verify_input('110101111011$hsajhahs@          @')
    verify_input('110101111011$hsajhahs@         @')
    verify_input('1101011111$hsajhahs@              @')