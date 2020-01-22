from aoc_2019.day11.computer import IntCodeComputer


def convert_to_ascii_ints(s):
    return [ord(c) for c in s]


def ascii_to_string(n):
    return str(chr(n))


def print_ascii_ints(ascii_ints):
    s = ''.join(ascii_to_string(n) for n in ascii_ints)
    print(s)


def print_outputs(ascii_ints):
    s = ''.join(ascii_to_string(n) for n in ascii_ints)

    maps = s.split('\n\n')
    print(f'There are {len(maps)} images.')
    for map in maps:
        print(map)
        print()


if __name__ == '__main__':

    with open('aoc_2019/day21/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    # Part I
    computer = IntCodeComputer(numbers)
    commands = [
        # Put T to 1
        "NOT A T",
        "OR A T",
        # if there is a hole in A, B or C, put T to 0
        "AND A T",
        "AND B T",
        "AND C T",
        # if hole in A, B or C, jump if D is not a hole
        "NOT T J",
        "AND D J",
        "WALK"
    ]

    inputs = []
    for command in commands:
        inputs.extend(convert_to_ascii_ints(command + '\n'))
    outputs = computer.execute(inputs)

    if outputs[-1] > 500:
        print(f'result part I: {outputs[-1]}')
    else:
        print_outputs(outputs)

    # Part II
    computer = IntCodeComputer(numbers)
    commands = [
        ## if (A=0 OR B=0 OR C=0) AND D=1, jump
        # Put T to 1
        "NOT A T",
        "OR A T",
        # if there is a hole in A, B or C, put T to 0
        "AND A T",
        "AND B T",
        "AND C T",
        # if hole in A, B or C, jump if D is not a hole
        "NOT T J",
        "AND D J",
        ## Put J to 0 if E=0 AND H=0
        # Put T to 0
        "NOT A T",
        "AND A T",
        # OR E H
        "OR E T",
        "OR H T",
        "AND T J",
        "RUN"
    ]

    inputs = []
    for command in commands:
        inputs.extend(convert_to_ascii_ints(command + '\n'))
    outputs = computer.execute(inputs)

    if outputs[-1] > 500:
        print(f'result part II: {outputs[-1]}')
    else:
        print_outputs(outputs)
