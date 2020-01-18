from aoc_2019.day11.computer import IntCodeComputer
from collections import Counter

D_UP    = '^'
D_DOWN  = 'v'
D_LEFT  = '<'
D_RIGHT = '>'
DIRECTIONS = {D_UP, D_DOWN, D_LEFT, D_RIGHT}

T_LEFT  = 'L'
T_RIGHT = 'R'

DELTAS = {
    D_UP   : (-1, 0),
    D_DOWN : (1, 0),
    D_LEFT : (0, -1),
    D_RIGHT: (0, 1)
}


def get_direction(current_direction, turn):
    assert turn in {T_LEFT, T_RIGHT}
    assert current_direction in DIRECTIONS

    if current_direction == D_UP:
        return D_LEFT if turn == T_LEFT else D_RIGHT
    elif current_direction == D_LEFT:
        return D_DOWN if turn == T_LEFT else D_UP
    elif current_direction == D_DOWN:
        return D_RIGHT if turn == T_LEFT else D_LEFT
    elif current_direction == D_RIGHT:
        return D_UP if turn == T_LEFT else D_DOWN



def ascii_to_string(n):
    return str(chr(n))


def print_ascii_ints(ascii_ints):
    s = ''.join(ascii_to_string(n) for n in ascii_ints)
    print(s)


def print_map(map):
    for line in map:
        print(''.join(line))


def convert_ascii_to_map(ascii_ints):
    s = ''.join(ascii_to_string(n) for n in ascii_ints)
    lines = [list(line) for line in s.split('\n') if line]
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c in DIRECTIONS:
                direction = c
                position = (i, j)
                line[j] = '#'
    return lines, position, direction


def print_outputs(ascii_ints):
    s = ''.join(ascii_to_string(n) for n in ascii_ints)

    maps = s.split('\n\n')
    print(f'There are {len(maps)} images.')
    for map in maps:
        print(map)
        print()


def find_intersections(map):
    nrow = len(map)
    ncol = len(map[0])
    intersections = []

    for row in range(1, nrow - 1):
        for col in range(1, ncol -1):
            if map[row][col] == '#':
                is_intersection = True
                for d in DIRECTIONS:
                    delta = DELTAS[d]
                    next_position = (row + delta[0], col + delta[1])
                    if map[next_position[0]][next_position[1]] != '#':
                        is_intersection = False
                if is_intersection:
                    intersections.append((row, col))
    return sum(row * col for row, col in intersections)


# PART II

def _is_inside_map(map, position):
    try:
        map[position[0]][position[1]]
        return True
    except IndexError:
        return False


def convert_map_to_movements(map, position, direction):
    """
    Starting from position, find a list of (direction, distance) pairs that
    will take to robot up to the end of the scaffolding.
    """

    for turn in [T_LEFT, T_RIGHT]:
        next_direction = get_direction(direction, turn)
        delta = DELTAS[next_direction]
        next_position = (position[0] + delta[0], position[1] + delta[1])

        # How far can we go in that direction?
        distance = 0

        while _is_inside_map(map, next_position) and map[next_position[0]][next_position[1]] == '#':
            next_position = (next_position[0] + delta[0], next_position[1] + delta[1])
            distance += 1

        if distance > 0:
            # We found a good turn
            next_position = (next_position[0] - delta[0], next_position[1] - delta[1])
            next_movements = convert_map_to_movements(map, next_position, next_direction)
            return [(turn, distance)] + next_movements

    # No good turn was found
    return []


def convert_to_ascii_ints(s):
    return [ord(c) for c in s]


if __name__ == '__main__':

    with open('aoc_2019/day17/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    computer = IntCodeComputer(numbers)
    outputs = computer.execute([])

    print(f'outputs_size: {len(outputs)}')

    print_ascii_ints(outputs)

    map, position, direction = convert_ascii_to_map(outputs)
    print_map(map)
    print(f'position: {position} - direction: {direction}')

    # PART I
    alignment_parameter = find_intersections(map)
    print(f'alignment_parameter: {alignment_parameter}')

    # PART II
    movements = convert_map_to_movements(map, position, direction)
    print(f'movements: {movements}')

    # Activate robot
    numbers[0] = 2
    computer = IntCodeComputer(numbers)

    main_routine = "A,A,B,C,A,C,B,C,A,B\n"
    A = "L,4,L,10,L,6\n"
    B = "L,6,L,4,R,8,R,8\n"
    C = "L,6,R,8,L,10,L,8,L,8\n"
    video_feed = "n\n"
    for i, s in enumerate([main_routine, A, B, C, video_feed]):
        outputs = computer.execute(convert_to_ascii_ints(s))
        print(f'step {i}')
        print_outputs(outputs)

        print(outputs[-20:])


    # # Count sequences of 1, 2, 3 or 4 elements
    # counter_1_movement  = Counter(movements)
    # counter_2_movements = Counter([tuple(movements[i:i+2]) for i in range(len(movements) - 1)])
    # counter_3_movements = Counter([tuple(movements[i:i+3]) for i in range(len(movements) - 2)])
    # counter_4_movements = Counter([tuple(movements[i:i+4]) for i in range(len(movements) - 3)])
    # counter_5_movements = Counter([tuple(movements[i:i+5]) for i in range(len(movements) - 4)])
    # print(counter_1_movement)
    # print(counter_2_movements)
    # print(counter_3_movements)
    # print(counter_4_movements)
    # print(counter_5_movements)




