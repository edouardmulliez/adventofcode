from collections import defaultdict
from enum import Enum, auto
from aoc_2019.day11.computer import IntCodeComputer

C_BLACK = 0
C_WHITE = 1

TURN_LEFT  = 0
TURN_RIGHT = 1


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


NEXT_DIRECTIONS = {
    (Direction.UP, TURN_LEFT): Direction.LEFT,
    (Direction.UP, TURN_RIGHT): Direction.RIGHT,
    (Direction.RIGHT, TURN_LEFT): Direction.UP,
    (Direction.RIGHT, TURN_RIGHT): Direction.DOWN,
    (Direction.DOWN, TURN_LEFT): Direction.RIGHT,
    (Direction.DOWN, TURN_RIGHT): Direction.LEFT,
    (Direction.LEFT, TURN_LEFT): Direction.DOWN,
    (Direction.LEFT, TURN_RIGHT): Direction.UP
}
DELTAS = {
    Direction.UP    : (-1, 0),
    Direction.DOWN  : (1, 0),
    Direction.LEFT  : (0, -1),
    Direction.RIGHT : (0, 1)
}


def get_next_state(position, direction, turn):
    next_direction = NEXT_DIRECTIONS[(direction, turn)]
    delta = DELTAS[next_direction]
    next_position = (position[0] + delta[0], position[1] + delta[1])

    return next_position, next_direction


def convert_color(color):
    if color == C_WHITE:
        return 'x'
    else:
        return ' '


def print_panel(panel):
    positions = list(panel.keys())
    row_min = min(row for row, col in positions)
    row_max = max(row for row, col in positions)
    col_min = min(col for row, col in positions)
    col_max = max(col for row, col in positions)

    map = []
    for row in range(row_min, row_max + 1):
        line = [panel[(row, col)] for col in range(col_min, col_max + 1)]
        map.append(line)

    for line in map:
        print(''.join(convert_color(c) for c in line))


def painting_robot(numbers):
    computer = IntCodeComputer(numbers)
    panel = defaultdict(int)
    position = (0, 0)
    direction = Direction.UP
    painted_positions = set()

    while not computer.is_finished:
        output_color, output_turn = computer.execute([panel[position]])

        # Question: do we consider that we can paint a black position in black?
        painted_positions.add(position)
        panel[position] = output_color

        next_position, next_direction = get_next_state(position, direction, output_turn)
        position = next_position
        direction = next_direction

    return len(painted_positions)


def painting_robot_part2(numbers):
    computer = IntCodeComputer(numbers)
    panel = defaultdict(int)
    position = (0, 0)
    direction = Direction.UP
    painted_positions = set()

    # paint first panel white
    panel[position] = C_WHITE

    while not computer.is_finished:
        output_color, output_turn = computer.execute([panel[position]])

        # Question: do we consider that we can paint a black position in black?
        painted_positions.add(position)
        panel[position] = output_color

        next_position, next_direction = get_next_state(position, direction, output_turn)
        position = next_position
        direction = next_direction

    return panel


if __name__ == '__main__':
    with open('aoc_2019/day11/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    nb_painted = painting_robot(numbers.copy())
    print(f'nb_painted: {nb_painted}')

    panel = painting_robot_part2(numbers.copy())
    print_panel(panel)

    # CODE: PGUEHCJH