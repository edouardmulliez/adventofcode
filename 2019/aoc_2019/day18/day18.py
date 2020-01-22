from collections import deque
from copy import deepcopy
import typing
from typing import Tuple


START = '@'
START_POSITIONS = set('1234')
WALL = '#'

def is_key(c: str):
    return c.islower()


def is_gate(c: str):
    return c.isupper()


def get_key_positions(map):
    key_positions = {}
    nrow = len(map)
    ncol = len(map[0])
    for i in range(nrow):
        for j in range(ncol):
            c = map[i][j]
            if is_key(c) or c == START or c in START_POSITIONS:
                key_positions[c] = (i, j)
    return key_positions


def get_neighbors(map, position):
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for delta in deltas:
        new_position = (position[0] + delta[0], position[1] + delta[1])
        try:
            c = map[new_position[0]][new_position[1]]
            if c != WALL:
                neighbors.append(new_position)
        except IndexError:
            pass
    return neighbors


def get_shortest_distances_from(map, origin: Tuple[int, int]):
    distances = {origin: 0}
    needed_keys = {origin: set()}
    visited = set()

    queue = deque([origin])

    while queue:
        node = queue.popleft()
        visited.add(node)

        for neighbor in get_neighbors(map, node):
            if neighbor not in visited:
                distances[neighbor] = distances[node] + 1
                needed_keys[neighbor] = deepcopy(needed_keys[node])
                c = map[neighbor[0]][neighbor[1]]
                if is_gate(c):
                    needed_keys[neighbor].add(c.lower())
                queue.append(neighbor)

    return distances, needed_keys


def get_shortest_distances(map):
    key_positions = get_key_positions(map)
    positions_to_keys = {position: key for key, position in key_positions.items()}

    all_distances = {}
    all_needed_keys = {}

    for from_key, from_pos in key_positions.items():
        distances, needed_keys = get_shortest_distances_from(map, from_pos)
        for to_pos, distance in distances.items():
            if to_pos in positions_to_keys:
                all_distances[(from_key, positions_to_keys[to_pos])] = distance
        for to_pos, needed_keys in needed_keys.items():
            if to_pos in positions_to_keys:
                all_needed_keys[(from_key, positions_to_keys[to_pos])] = needed_keys

    return all_distances, all_needed_keys


def get_optimal_distance(
    optimal_distances,
    distances, needed_keys, current_key: str, taken_keys: typing.AbstractSet[str], remaining_keys):
    arg_hash = (current_key, frozenset(taken_keys))
    if arg_hash in optimal_distances:
        return optimal_distances[arg_hash]

    if not remaining_keys:
        return 0

    min_distance = None
    for next_key in remaining_keys:
        if taken_keys >= needed_keys[(current_key, next_key)]:
            # next_key can be reached with taken_keys
            distance = get_optimal_distance(
                optimal_distances,
                distances=distances,
                needed_keys=needed_keys,
                current_key=next_key,
                taken_keys=taken_keys | {next_key},
                remaining_keys=remaining_keys - {next_key}
            )
            if distance is not None:
                distance += distances[(current_key, next_key)]
                if min_distance is None or distance < min_distance:
                    min_distance = distance

    optimal_distances[arg_hash] = min_distance
    return min_distance


def init_map_for_part2(map):
    map = [list(row) for row in map]
    nrow = len(map)
    ncol = len(map[0])
    for i in range(nrow):
        for j in range(ncol):
            if map[i][j] == START:
                start_position = (i, j)
    center = [
        '1#2',
        '###',
        '3#4'
    ]
    for i in range(3):
        for j in range(3):
            map[start_position[0] + i - 1][start_position[1] + j - 1] = center[i][j]
    return map


def get_optimal_distance_part2(
    optimal_distances,
    distances, needed_keys, current_keys: str, taken_keys: typing.AbstractSet[str], remaining_keys):

    arg_hash = (tuple(current_keys), frozenset(taken_keys))
    if arg_hash in optimal_distances:
        return optimal_distances[arg_hash]

    if not remaining_keys:
        return 0

    min_distance = None
    for next_key in remaining_keys:
        for robot in range(4):
            current_key = current_keys[robot]
            try:
                if taken_keys >= needed_keys[(current_key, next_key)]:
                    # next_key can be reached with taken_keys
                    next_keys = list(current_keys)
                    next_keys[robot] = next_key
                    distance = get_optimal_distance_part2(
                        optimal_distances,
                        distances=distances,
                        needed_keys=needed_keys,
                        current_keys=next_keys,
                        taken_keys=taken_keys | {next_key},
                        remaining_keys=remaining_keys - {next_key}
                    )
                    if distance is not None:
                        distance += distances[(current_key, next_key)]
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
            except KeyError:
                pass

    optimal_distances[arg_hash] = min_distance
    return min_distance




if __name__ == '__main__':
    with open('aoc_2019/day18/input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        map = [line for line in lines if line]

    # # Part I
    # key_positions = get_key_positions(map)
    # start_position = key_positions[START]

    # distances, needed_keys = get_shortest_distances(map)

    # remaining_keys = set_remove(key_positions.keys(), START)
    # optimal_distance = get_optimal_distance({}, distances, needed_keys, START, set(), remaining_keys)

    # print(distances)
    # print(needed_keys)
    # print(optimal_distance)

    # Part II

    map = init_map_for_part2(map)

    distances, needed_keys = get_shortest_distances(map)
    key_positions = get_key_positions(map)

    current_keys = list('1234')
    remaining_keys = set(key_positions.keys()) - START_POSITIONS

    optimal_distance = get_optimal_distance_part2(
        {}, distances, needed_keys, current_keys, set(), remaining_keys
    )

    print(optimal_distance)


