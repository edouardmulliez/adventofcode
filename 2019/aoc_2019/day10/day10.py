from collections import defaultdict
import math


def pgcd(a,b):
    if b==0:
        return a
    else:
        r = a % b
        return pgcd(b,r)


FULL = '#'


def get_angle_from_top(row, col):
    angle = math.atan2(row, col)
    return (angle + math.pi / 2) % (2 * math.pi)


def count_visible_asteroids(map, row, col, nb_row, nb_col):
    if map[row][col] != FULL:
        return 0
    directions = set()
    for i in range(nb_row):
        for j in range(nb_col):
            if i != row or j != col:
                if map[i][j] == FULL:
                    row_diff = i - row
                    col_diff = j - col
                    d = pgcd(abs(row_diff), abs(col_diff))
                    directions.add((row_diff // d, col_diff // d))

    return len(directions)


def get_directions_to_asteroids(map, row, col, nb_row, nb_col):
    direction_to_asteroids = defaultdict(list)
    for i in range(nb_row):
        for j in range(nb_col):
            if i != row or j != col:
                if map[i][j] == FULL:
                    row_diff = i - row
                    col_diff = j - col
                    d = pgcd(abs(row_diff), abs(col_diff))
                    direction_to_asteroids[(row_diff // d, col_diff // d)].append((row_diff, col_diff))

    return direction_to_asteroids


def _get_sorted_asteroids(directions_to_asteroids):
    angle_to_asteroids = [
        (get_angle_from_top(direction[0], direction[1]), asteroids)
        for direction, asteroids in directions_to_asteroids.items()
    ]
    angle_to_asteroids.sort(key=lambda x: x[0])

    for i in range(len(angle_to_asteroids)):
        asteroids = angle_to_asteroids[i][1]
        asteroids.sort(key=lambda x: sum(abs(item) for item in x))

    asteroids_per_angle =[asteroids for angle, asteroids in angle_to_asteroids]

    sorted_asteroids = extract_in_sorted_order(asteroids_per_angle)
    return sorted_asteroids


def get_sorted_asteroids(map):
    _, max_position = get_max_visible_asteroids(map)
    nb_row = len(map)
    nb_col = len(map[0])
    directions_to_asteroids = get_directions_to_asteroids(map, max_position[0], max_position[1], nb_row, nb_col)
    sorted_asteroids = _get_sorted_asteroids(directions_to_asteroids)
    return sorted_asteroids


def extract_in_sorted_order(asteroids_per_angle):
    sorted_asteroids = []

    while True:
        is_empty = True
        for asteroids in asteroids_per_angle:
            if asteroids:
                is_empty = False
                sorted_asteroids.append(asteroids.pop(0))
        if is_empty:
            return sorted_asteroids


def get_max_visible_asteroids(map):
    nb_row = len(map)
    nb_col = len(map[0])
    max_nb_asteroids = 0
    max_position = None
    for i in range(nb_row):
        for j in range(nb_col):
            nb_asteroids = count_visible_asteroids(map, i, j, nb_row, nb_col)
            if nb_asteroids > max_nb_asteroids:
                max_nb_asteroids = nb_asteroids
                max_position = (i, j)

    return max_nb_asteroids, max_position


# Tests

def test_get_angle_from_top():
    assert get_angle_from_top(-1, 0) < get_angle_from_top(-1, 1) < get_angle_from_top(0, 1) < get_angle_from_top(1, 1)
    assert get_angle_from_top(1, 1) < get_angle_from_top(1, 0) < get_angle_from_top(1, -1) < get_angle_from_top(0, -1) < get_angle_from_top(-1, -1)
    assert get_angle_from_top(0, -1) < get_angle_from_top(-1, -1)


def test_extract_in_sorted_order():
    asteroids_per_angle = [
        [1],
        [2, 5],
        [3],
        [4, 6, 7]
    ]
    asteroids = extract_in_sorted_order(asteroids_per_angle)
    assert asteroids == [1, 2, 3, 4, 5, 6, 7]



if __name__ == '__main__':

    with open('aoc_2019/day10/input.txt') as f:
        map = [line.strip() for line in f.readlines()]

    max_nb_asteroids, max_position = get_max_visible_asteroids(map)
    print(f'max_nb_asteroids: {max_nb_asteroids}')
    print(f'max_position: {max_position}')

    sorted_asteroids = get_sorted_asteroids(map)
    chosen_asteroid = sorted_asteroids[200 - 1]
    chosen_row = chosen_asteroid[0] + max_position[0]
    chosen_col = chosen_asteroid[1] + max_position[1]
    print(f'chosen_row: {chosen_row}, chosen_col: {chosen_col}')
    print(f'result: {chosen_col * 100 + chosen_row}')

