from copy import deepcopy
import numpy as np
from scipy.signal import convolve2d


BUG = '#'
EMPTY = '.'


def char_to_int(c):
    if c == BUG:
        return 1
    elif c == EMPTY:
        return 0
    else:
        raise ValueError(f"Invalid character: {c}")


NEIGHBOR_MASK = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
], dtype=int)

INNER_MASK = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
])

OUTER_MASK = np.array([
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
])


def get_rating_mask(nrow, ncol):
    mask = np.zeros((nrow, ncol), dtype=int)
    for i in range(nrow):
        for j in range(ncol):
            idx = j + i * ncol
            mask[i, j] = 2 ** idx
    return mask


def get_rating(map, rating_mask):
    return (map * rating_mask).sum()


def get_next_state(map):
    neighbor_counts = convolve2d(map, NEIGHBOR_MASK, mode='same')
    nrow, ncol = map.shape
    next_map = np.zeros((nrow, ncol), dtype=int)
    for i in range(nrow):
        for j in range(ncol):
            if map[i, j] == 1:
                if neighbor_counts[i, j] == 1:
                    value = 1
                else:
                    value = 0
            else:
                if 1 <= neighbor_counts[i, j] <= 2:
                    value = 1
                else:
                    value = 0
            next_map[i, j] = value
    return next_map


def part_1(map):
    nrow, ncol = map.shape
    rating_mask = get_rating_mask(nrow, ncol)

    ratings = set()
    i = 0
    while True:
        rating = get_rating(map, rating_mask)
        if rating in ratings:
            return rating
        ratings.add(rating)

        map = get_next_state(map)
        i += 1


def has_inner_bug(map):
    return (map * INNER_MASK).any()


def has_outer_bug(map):
    return (map * OUTER_MASK).any()


def create_adjacent_maps(maps):
    min_level = min(maps)
    max_level = max(maps)
    if has_inner_bug(maps[max_level]):
        max_level += 1
        maps[max_level] = np.zeros(map.shape, dtype=int)
    if has_outer_bug(maps[min_level]):
        min_level -= 1
        maps[min_level] = np.zeros(map.shape, dtype=int)


def get_neighbor_bugs(maps, i, j, level):
    min_level = min(maps)
    max_level = max(maps)
    map = maps[level]
    nrow, ncol = map.shape
    middle = 2
    neighbor_counts = convolve2d(map, NEIGHBOR_MASK, mode='same')
    # Same level bugs
    bug_count = neighbor_counts[i, j]

    if OUTER_MASK[i, j] and level > min_level:
        outer_map = maps[level - 1]
        if i == 0:
            bug_count += outer_map[1, middle]
        elif i == nrow - 1:
            bug_count += outer_map[3, middle]
        if j == 0:
            bug_count += outer_map[middle, 1]
        elif j == ncol - 1:
            bug_count += outer_map[middle, 3]

    if INNER_MASK[i, j] and level < max_level:
        inner_map = maps[level + 1]
        if i == 1 and j == middle:
            # add top of inner map
            bug_count += inner_map[0, :].sum()
        elif i == 3 and j == middle:
            # add bottom of inner map
            bug_count += inner_map[nrow - 1, :].sum()
        elif i == middle and j == 1:
            # add left part of inner map
            bug_count += inner_map[:, 0].sum()
        elif i == middle and j == 3:
            # add right part of inner map
            bug_count += inner_map[:, ncol - 1].sum()

    return bug_count


def update_maps(maps):
    nrow, ncol = maps[0].shape

    next_maps = deepcopy(maps)

    for level, map in maps.items():
        for i in range(nrow):
            for j in range(ncol):
                if i == j == 2:
                    # The middle of the map is a special case
                    continue
                neighbor_bugs = get_neighbor_bugs(maps, i, j, level)
                if map[i, j] == 1:
                    if neighbor_bugs == 1:
                        value = 1
                    else:
                        value = 0
                else:
                    if 1 <= neighbor_bugs <= 2:
                        value = 1
                    else:
                        value = 0
                next_maps[level][i, j] = value
    return next_maps


def part_2(map, nb_steps):
    maps = {0: map}

    print_maps(maps)
    for _ in range(nb_steps):
        # Create any needed adjacent map (on higher or lower level)
        create_adjacent_maps(maps)
        maps = update_maps(maps)

    bug_count = sum(map.sum() for map in maps.values())
    return bug_count


def print_maps(maps):
    for level, map in maps.items():
        print(f'level: {level}')
        print(map)


if __name__ == '__main__':

    with open('aoc_2019/day24/input.txt') as f:
        map = [row.strip() for row in f.readlines()]

    map = [list(row) for row in map if row]
    map = [
        [char_to_int(c) for c in row]
        for row in map
    ]
    map = np.array(map, dtype=int)

    rating = part_1(map)
    print(f'PART I - rating: {rating}')

    nb_steps = 200
    bug_count = part_2(map, nb_steps)
    print(f'PART II - bug_count: {bug_count}')
