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


class IntCodeComputer:

    def __init__(self, memory):
        self.memory = defaultdict(int)
        for i, number in enumerate(memory):
            self.memory[i] = number

        self.is_finished = False
        self.base_index = 0
        self.position = 0


    def execute(self, inputs):
        """
        Executes the program up to the point where a next input is needed or up to the end
        of the program. It returns the outputs produced during the execution.
        """
        outputs = []
        while True:
            modes_and_op = self.memory[self.position]
            op, modes = extract_modes_and_op(modes_and_op)

            assert op in FLAGS

            parameters = []
            for i, mode in enumerate(modes):
                assert mode in MODES
                parameter = self.memory[self.position + 1 + i]

                if mode == MODE_POSITION and not is_parameter_for_assignment(op, i):
                    parameter = self.memory[parameter]
                if mode == MODE_RELATIVE:
                    parameter += self.base_index
                    if not is_parameter_for_assignment(op, i):
                        parameter = self.memory[parameter]

                parameters.append(parameter)

            if op not in FLAGS:
                raise ValueError(f'Incorrect op: {op}')

            if op == F_END:
                self.is_finished = True
                break
            elif op == F_ADD:
                self.memory[parameters[2]] = parameters[0] + parameters[1]
            elif op == F_MUL:
                self.memory[parameters[2]] = parameters[0] * parameters[1]
            elif op == F_IN:
                if inputs:
                    self.memory[parameters[0]] = inputs.pop(0)
                else:
                    break
            elif op == F_OUT:
                outputs.append(parameters[0])
            elif op == F_LESS:
                if parameters[0] < parameters[1]:
                    self.memory[parameters[2]] = 1
                else:
                    self.memory[parameters[2]] = 0
            elif op == F_EQUAL:
                if parameters[0] == parameters[1]:
                    self.memory[parameters[2]] = 1
                else:
                    self.memory[parameters[2]] = 0
            elif op == F_BASE_ADD:
                self.base_index += parameter

            self.position = get_next_pointer_position(self.position, op, parameters)

        return outputs


# Tests

def test_computer():

    computer = IntCodeComputer([3,3,1108,-1,8,3,4,3,99])
    assert computer.execute([8]) == [1]
    assert computer.is_finished

    computer = IntCodeComputer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
    assert computer.execute([]) == []
    assert not computer.is_finished
    assert computer.execute([3]) == [1]
    assert computer.is_finished

