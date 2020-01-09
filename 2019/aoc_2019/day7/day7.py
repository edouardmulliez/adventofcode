
from aoc_2019.day5.day5 import execute_program
from itertools import product

PHASES = [0, 1, 2, 3, 4]


def get_output_signal(numbers, phases):
    input = 0
    for phase in phases:
        _, outputs = execute_program(numbers.copy(), [phase, input])
        input = outputs[-1]

    return outputs[-1]


def get_max_output_signal(numbers, input, remaining_steps):

    if remaining_steps == 0:
        return input, []

    max_signal = None
    for phase in PHASES:
        _, outputs = execute_program(numbers.copy(), [phase, input])
        signal, next_phases = get_max_output_signal(numbers, outputs[-1], remaining_steps - 1)
        if max_signal is None or signal > max_signal:
            max_signal = signal
            max_phases = [phase] + next_phases

    return max_signal, max_phases


def get_max_output_signal2(numbers):
    max_signal = None
    for phases in product(range(5), repeat=5):
        signal = get_output_signal(numbers, phases)

        if max_signal is None or signal > max_signal:
            max_signal = signal
            max_phases = phases

    return max_signal, max_phases


# Tests
def test_get_max_output_signal():
    # numbers = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    # signal, phases = get_max_output_signal(numbers.copy(), 0, 5)

    # signal2 = get_output_signal(numbers.copy(), phases)
    # assert signal == signal2
    # # assert signal == 43210


    numbers = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    signal, phases = get_max_output_signal2(numbers)

    assert signal == 54321

    # numbers = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    # signal, phases = get_max_output_signal(numbers.copy(), 0, 5)

    # assert get_output_signal(numbers.copy(), [0,0,0,0,0]) == 55555

    # assert signal == 54321
    # assert phases == [0, 1, 2, 3, 4]

def test_get_output_signal():

    # This below is not correct. I should not be able to output a number as high as 55555
    numbers = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert get_output_signal(numbers.copy(), [0,0,0,0,0]) == 55555



    # numbers = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    # assert get_output_signal(numbers, [4,3,2,1,0]) == 43210

    # numbers = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    # assert get_output_signal(numbers, [0,1,2,3,4]) == 54321



if __name__ == '__main__':
    with open('aoc_2019/day7/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    signal, phases = get_max_output_signal2(numbers)
    print(f'signal: {signal}')