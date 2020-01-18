import random
from aoc_2019.day11.computer import IntCodeComputer


class Direction:
    NORTH = 1
    SOUTH = 2
    WEST  = 3
    EAST  = 4


class Status:
    WALL   = 0
    EMPTY  = 1
    OXYGEN = 2


DELTAS = {
    Direction.NORTH: ( 0,-1),
    Direction.SOUTH: ( 0, 1),
    Direction.WEST : (-1, 0),
    Direction.EAST : ( 1, 0)
}



def update_map_and_position(map, position, direction, status):
    delta = DELTAS[direction]
    next_position = (position[0] + delta[0], position[1] + delta[1])
    map[next_position] = status
    if status == Status.WALL:
        return position
    else:
        return next_position


# Keep track of positions/states with some unknown neighbors. When blocked, go back to them.
# If there is an unknown position around, go there. If not, choose among there positions.
def get_unknown_directions(map, position):
    unknown_directions = []
    for d in range(1, 4 + 1):
        delta = DELTAS[d]
        next_position = (position[0] + delta[0], position[1] + delta[1])
        if next_position not in map:
            unknown_directions.append(d)
    return unknown_directions


def explore(map, position, computer: IntCodeComputer):
    """
    We start with an empty map of the ship. The goal is to obtain a full map of the ship
    by making the droid explore it.
    """
    # We keep track of the positions where there is some unknown directions around
    starting_points = {}

    i = 0

    while True:
        if i % 1000 == 0:
            print(i)
        unknown_directions = get_unknown_directions(map, position)
        # Update starting points
        if len(unknown_directions) > 1:
            if position not in starting_points:
                starting_points[position] = computer.memory.copy()
        else:
            if position in starting_points:
                del starting_points[position]

        # Explore from that point or choose a new starting point
        if unknown_directions:
            d = unknown_directions[0]
            status = computer.execute([d])[0]
            position = update_map_and_position(map, position, d, status)
        else:
            if starting_points:
                position, memory = next(iter(starting_points.items()))
                computer.memory = memory
            else:
                return True

        i += 1


def status_to_string(status: str):
    if status == Status.WALL:
        return '#'
    elif status == Status.EMPTY:
        return '.'
    elif status == Status.OXYGEN:
        return 'O'


def print_map(map, position):
    x_min = min([x for x, y in map.keys()])
    x_max = max([x for x, y in map.keys()])
    y_min = min([y for x, y in map.keys()])
    y_max = max([y for x, y in map.keys()])
    for y in range(min(y_min,0), y_max + 1):
        line = []
        for x in range(min(x_min,0), x_max + 1):
            try:
                c = status_to_string(map[(x,y)])
            except KeyError:
                c = ' '
            if (x, y) == position:
                c = 'D'
            line.append(c)
        print(''.join(line))


def shortest_distance_to_oxygen(map, position, visited=None):
    if visited is None:
        visited = set()
    visited.add(position)
    if map[position] == Status.OXYGEN:
        return 0

    min_distance = None
    for d in range(1, 4 + 1):
        delta = DELTAS[d]
        next_position = (position[0] + delta[0], position[1] + delta[1])
        if next_position not in visited and map[next_position] != Status.WALL:
            remaining_distance = shortest_distance_to_oxygen(map, next_position, visited)
            if remaining_distance is not None:
                if min_distance is None or remaining_distance < min_distance:
                    min_distance = remaining_distance

    if min_distance is not None:
        return 1 + min_distance
    else:
        return None


def has_oxygen_neighbor(map, position):
    for d in range(1, 4 + 1):
        delta = DELTAS[d]
        next_position = (position[0] + delta[0], position[1] + delta[1])
        if map[next_position] == Status.OXYGEN:
            return True


def get_positions_to_fill(map):
    """
    Returns a list of positions to fill with oxygen.
    """
    positions_to_fill = []
    for position, status in map.items():
        if status == Status.EMPTY and has_oxygen_neighbor(map, position):
            positions_to_fill.append(position)
    return positions_to_fill


def get_steps_to_fill_oxygen(map):
    step_nb = 0

    while True:
        positions_to_fill = get_positions_to_fill(map)
        if not positions_to_fill:
            return step_nb
        for position in positions_to_fill:
            map[position] = Status.OXYGEN
        step_nb += 1


if __name__ == '__main__':
    with open('aoc_2019/day15/input.txt') as f:
        numbers = [int(n) for n in f.readline().split(',')]

    computer = IntCodeComputer(numbers)
    position = (0, 0)
    map = {position: Status.EMPTY}

    # PART I
    explore(map, position, computer)
    print_map(map, position)

    print("Looking for shortest path...")

    min_distance = shortest_distance_to_oxygen(map, (0, 0))
    print(f'min_distance: {min_distance}')

    # PART II

    steps_for_oxygen = get_steps_to_fill_oxygen(map.copy())
    print(f'steps_for_oxygen: {steps_for_oxygen}')

    # I tried: 352, 335 (too high), 309 / Not working :-(

