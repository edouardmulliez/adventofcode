from aoc_2019.day11.computer import IntCodeComputer
from itertools import product



T_EMPTY  = 0
T_WALL   = 1
T_BLOCK  = 2
T_PADDLE = 3
T_BALL   = 4

D_LEFT = -1
D_NOTHING = 0
D_RIGHT = 1

INPUT_DIRECTIONS = {D_LEFT, D_NOTHING, D_RIGHT}


def get_score(outputs):
    idx = 0
    while idx + 8 < len(outputs):
        if (
            outputs[idx] == -1 and outputs[idx + 1] == 0
            and outputs[idx + 3] == -1 and outputs[idx + 4] == 0
            and outputs[idx + 6] == -1 and outputs[idx + 7] == 0
            ):
            return outputs[idx + 8]
        idx += 3


def get_map(outputs, map=None):
    map = map or {}
    block_nb = 0
    idx = 0
    while idx < len(outputs):
        x = outputs[idx]
        y = outputs[idx + 1]
        tile_id = outputs[idx + 2]

        # assert (x,y) not in map
        map[(x,y)] = tile_id

        if tile_id == T_BLOCK:
            block_nb += 1

        idx += 3

    return map


def part1(numbers):
    computer = IntCodeComputer(numbers)
    outputs = computer.execute([])

    assert computer.is_finished

    map = get_map(outputs)
    block_nb = sum([tile_id == T_BLOCK for tile_id in map.values()])

    return block_nb


def tile_to_string(tile_id):
    if tile_id == T_EMPTY:
        return ' '
    elif tile_id == T_PADDLE:
        return 'T'
    elif tile_id == T_WALL:
        return '|'
    elif tile_id == T_BALL:
        return 'o'
    elif tile_id == T_BLOCK:
        return 'x'
    else:
        raise ValueError(f'Incorrect tile_id: {tile_id}')


def print_map(map):
    x_min = max([x for x, y in map.keys()])
    x_max = max([x for x, y in map.keys()])
    y_min = min([y for x, y in map.keys()])
    y_max = max([y for x, y in map.keys()])
    for y in range(min(y_min,0), y_max + 1):
        line = []
        for x in range(min(x_min,0), x_max + 1):
            try:
                c = tile_to_string(map[(x,y)])
            except KeyError:
                c = ' '
            line.append(c)
        print(''.join(line))


def find_moves(memory, nb_moves):
    """
    The goal is to find nb_moves move which allows to not terminate the program.
    """
    if nb_moves == 0:
        return True, []
    computer = IntCodeComputer([])

    for move in range(-1, 2):
        computer.memory = memory.copy()
        computer.execute([move])
        if not computer.is_finished:
            success, moves = find_moves(computer.memory, nb_moves - 1)
            if success:
                return True, [move] + moves

    return False, []


def auto_part2(numbers):
    computer = IntCodeComputer(numbers)
    outputs = computer.execute([])

    map = get_map(outputs)

    print_map(map)
    print(f'score: {get_score(outputs)}')

    print('compute next moves')
    next_moves = find_moves(computer.memory, 10)
    print(f'next_moves: {next_moves}')

    moves = [-1, 0, 1, 1, 1, 1, 1, 1, 1, -1]
    for move in moves:
        outputs = computer.execute([move])
        map = get_map(outputs, map)
        print_map(map)
        print(f'score: {get_score(outputs)}')



def play_part2(numbers):
    computer = IntCodeComputer(numbers)
    outputs = computer.execute([])

    map = get_map(outputs)

    print_map(map)
    print(f'score: {get_score(outputs)}')

    while not computer.is_finished:
        direction = input('Enter Q, S or D:')

        DIRECTIONS = {
            'Q': -1,
            'S': 0,
            'D': 1
        }

        outputs = computer.execute([DIRECTIONS[direction]])
        map = get_map(outputs, map)
        print_map(map)
        print(f'score: {get_score(outputs)}')

    print('Game is finished')



# Idea:
# - find a suite of N moves which do not lead to program ending.
# - apply N/2 moves
# - repeat
# Question: how do we choose N?


if __name__ == '__main__':
    with open('aoc_2019/day13/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    # Part I
    block_nb = part1(numbers)
    print(f'block_nb: {block_nb}')

    # Part II

    # Insert 2 quarters
    numbers[0] = 2

    auto_part2(numbers)


    # play_part2(numbers)




