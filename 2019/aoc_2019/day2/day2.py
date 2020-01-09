
with open('input.txt') as f:
    line = f.readline()
    initial_numbers = [int(n) for n in line.strip().split(',')]


F_ADD = 1
F_MUL = 2
F_END = 99
FLAGS = {F_ADD, F_MUL, F_END}


def execute_program(numbers):
    position = 0
    while numbers[position] != F_END:
        op = numbers[position]
        a = numbers[numbers[position + 1]]
        b = numbers[numbers[position + 2]]
        result_index = numbers[position + 3]

        assert op in FLAGS
        if op == F_ADD:
            numbers[result_index] = a + b
        elif op == F_MUL:
            numbers[result_index] = a * b

        position += 4

    return numbers


assert execute_program([1,0,0,0,99]) == [2,0,0,0,99]
assert execute_program([2,3,0,3,99]) == [2,3,0,6,99]
assert execute_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert execute_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]


numbers = initial_numbers.copy()

def put_to_alarm_state(numbers):
    numbers[1] = 12
    numbers[2] = 2


put_to_alarm_state(numbers)
execute_program(numbers)
print(f"Solution for part 1: {numbers[0]}")


def is_input_pair_correct(noun, verb):
    EXPECTED_RESULT = 19690720
    numbers = initial_numbers.copy()
    numbers[1] = noun
    numbers[2] = verb
    try:
        execute_program(numbers)
        return numbers[0] == EXPECTED_RESULT
    except (AssertionError, IndexError) as e:
        print(f"Program execution failed for {noun}, {verb}")
        return False


def find_input_pair():
    for noun in range(100):
        for verb in range(100):
            if is_input_pair_correct(noun, verb):
                return noun, verb


noun, verb = find_input_pair()
print(f"Solution for part 2 - noun: {noun} - verb: {verb} - result: {100 * noun + verb}")
