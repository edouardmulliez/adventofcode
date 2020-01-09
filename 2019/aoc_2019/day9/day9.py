from collections import defaultdict

F_ADD    = 1
F_MUL    = 2
F_IN     = 3
F_OUT    = 4
F_JUMP_T = 5
F_JUMP_F = 6
F_LESS   = 7
F_EQUAL  = 8
F_BASE_ADD = 9
F_END    = 99

FLAGS = {F_ADD, F_MUL, F_IN, F_OUT, F_JUMP_T, F_JUMP_F, F_LESS, F_EQUAL, F_BASE_ADD, F_END}

MODE_POSITION = 0
MODE_VALUE    = 1
MODE_RELATIVE = 2

MODES = {MODE_POSITION, MODE_VALUE, MODE_RELATIVE}

PARAMETER_NB = {
    F_ADD   : 3,
    F_MUL   : 3,
    F_IN    : 1,
    F_OUT   : 1,
    F_JUMP_T: 2,
    F_JUMP_F: 2,
    F_LESS  : 3,
    F_EQUAL : 3,
    F_BASE_ADD: 1,
    F_END   : 0
}



def is_parameter_for_assignment(op, parameter_index):
    if op == F_IN:
        return parameter_index == 0
    elif op in [F_ADD, F_MUL, F_LESS, F_EQUAL]:
        return parameter_index == 2


def extract_modes_and_op(modes_and_op):
    op = modes_and_op % 100
    parameter_nb = PARAMETER_NB[op]

    modes = []
    modes_and_op = modes_and_op // 100
    for _ in range(parameter_nb):
        mode = modes_and_op % 10
        modes.append(mode)
        modes_and_op = modes_and_op // 10

    return op, modes


def get_next_pointer_position(position, op, parameters):
    next_position = position + 1 + PARAMETER_NB[op]

    if (op == F_JUMP_T and parameters[0] > 0) or (op == F_JUMP_F and parameters[0] == 0):
        next_position = parameters[1]

    return next_position


def execute_program(numbers, inputs):

    memory = defaultdict(int)
    for i, number in enumerate(numbers):
        memory[i] = number

    base_index = 0
    input_index = 0
    position = 0
    outputs = []
    while True:
        modes_and_op = memory[position]
        op, modes = extract_modes_and_op(modes_and_op)

        assert op in FLAGS

        parameters = []
        for i, mode in enumerate(modes):
            assert mode in MODES
            parameter = memory[position + 1 + i]

            if mode == MODE_POSITION and not is_parameter_for_assignment(op, i):
                parameter = memory[parameter]
            if mode == MODE_RELATIVE:
                parameter += base_index
                if not is_parameter_for_assignment(op, i):
                    parameter = memory[parameter]

            parameters.append(parameter)

        if op not in FLAGS:
            raise ValueError(f'Incorrect op: {op}')

        if op == F_END:
            break
        elif op == F_ADD:
            memory[parameters[2]] = parameters[0] + parameters[1]
        elif op == F_MUL:
            memory[parameters[2]] = parameters[0] * parameters[1]
        elif op == F_IN:
            memory[parameters[0]] = inputs[input_index]
            input_index += 1
        elif op == F_OUT:
            outputs.append(parameters[0])
        elif op == F_LESS:
            if parameters[0] < parameters[1]:  # is equal case?  --> TO BE CHECKED
                memory[parameters[2]] = 1
            else:
                memory[parameters[2]] = 0
        elif op == F_EQUAL:
            if parameters[0] == parameters[1]:
                memory[parameters[2]] = 1
            else:
                memory[parameters[2]] = 0
        elif op == F_BASE_ADD:
            base_index += parameter

        position = get_next_pointer_position(position, op, parameters)

    return memory, outputs


# Tests

def test_extract_modes_and_op():
    assert extract_modes_and_op(1)    == (1, [0, 0, 0])
    assert extract_modes_and_op(102)  == (2, [1, 0, 0])
    assert extract_modes_and_op(1002) == (2, [0, 1, 0])
    assert extract_modes_and_op(3)    == (3, [0])
    assert extract_modes_and_op(4)    == (4, [0])
    assert extract_modes_and_op(99)   == (99, [])


def test_execute_program():

    assert execute_program([3,9,8,9,10,9,4,9,99,-1,8], [8])[1][-1] == 1
    assert execute_program([3,9,8,9,10,9,4,9,99,-1,8], [10])[1][-1] == 0
    assert execute_program([3,9,8,9,10,9,4,9,99,-1,8], [5])[1][-1] == 0

    assert execute_program([3,9,7,9,10,9,4,9,99,-1,8], [5])[1][-1] == 1
    assert execute_program([3,9,7,9,10,9,4,9,99,-1,8], [10])[1][-1] == 0

    assert execute_program([3,3,1108,-1,8,3,4,3,99], [8])[1][-1] == 1
    assert execute_program([3,3,1108,-1,8,3,4,3,99], [7])[1][-1] == 0
    assert execute_program([3,3,1108,-1,8,3,4,3,99], [9])[1][-1] == 0

    assert execute_program([3,3,1107,-1,8,3,4,3,99], [7])[1][-1] == 1
    assert execute_program([3,3,1107,-1,8,3,4,3,99], [9])[1][-1] == 0

    assert execute_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0])[1][-1] == 0
    assert execute_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [13])[1][-1] == 1
    assert execute_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [-3])[1][-1] == 1

    assert execute_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0])[1][-1] == 0
    assert execute_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [3])[1][-1] == 1

    numbers = [
        3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,
        20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
    ]

    assert execute_program(numbers.copy(), [7])[1][-1] == 999
    assert execute_program(numbers.copy(), [8])[1][-1] == 1000
    assert execute_program(numbers.copy(), [9])[1][-1] == 1001

    # Day 9

    assert execute_program([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [])[1] == [
        109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
    ]

    outputs = execute_program([1102,34915192,34915192,7,4,7,99,0], [12])[1]
    assert len(outputs) == 1
    assert len(str(outputs[0])) == 16

    assert execute_program([104,1125899906842624,99], [12, 123])[1] == [1125899906842624]


test_execute_program()

if __name__ == '__main__':
    with open('aoc_2019/day9/input.txt') as f:
        line = f.readline()
        initial_numbers = [int(n) for n in line.strip().split(',')]

    numbers, outputs = execute_program(initial_numbers.copy(), [1])
    print(f'outputs for input 1: {outputs}')

    numbers, outputs = execute_program(initial_numbers.copy(), [2])
    print(f'outputs for input 2: {outputs}')
