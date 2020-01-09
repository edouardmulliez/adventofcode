"""
https://adventofcode.com/2019/day/3
ed.mulliez@gmail.com
"""

DELTA = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

def convert_to_positions(directions):
    positions = [(0, 0)]

    for direction, n in directions:
        position = positions[-1]
        delta = DELTA[direction]
        new_position = (position[0] + n * delta[0], position[1] + n * delta[1])
        positions.append(new_position)

    return positions


def get_intersections(positions_a, positions_b):
    intersections = set()

    for i_a in range(len(positions_a) - 1):
        for i_b in range(len(positions_b) - 1):
            intersection = get_intersection(
                positions_a[i_a], positions_a[i_a + 1],
                positions_b[i_b], positions_b[i_b + 1]
            )
            if intersection:
                intersections.add(intersection)

    return intersections



def get_delays(positions):
    delays = [0]
    for i in range(len(positions) - 1):
        pos = positions[i]
        next_pos = positions[i+1]
        next_delay = delays[-1] + manathan_distance_2_point(pos, next_pos)
        delays.append(next_delay)

    return delays


def manathan_distance_2_point(position_a, positions_b):
    return abs(positions_b[0] - position_a[0]) + abs(positions_b[1] - position_a[1])


def get_intersections_with_min_delay(positions_a, positions_b):
    # Get for each position of the wire, the delay
    delays_a = get_delays(positions_a)
    delays_b = get_delays(positions_b)

    min_delay = None

    for i_a in range(len(positions_a) - 1):
        for i_b in range(len(positions_b) - 1):
            intersection = get_intersection(
                positions_a[i_a], positions_a[i_a + 1],
                positions_b[i_b], positions_b[i_b + 1]
            )
            if intersection:
                delay_a = delays_a[i_a] + manathan_distance_2_point(positions_a[i_a], intersection)
                delay_b = delays_b[i_b] + manathan_distance_2_point(positions_b[i_b], intersection)
                delay = delay_a + delay_b

                if delay > 0:
                    if min_delay is None or min_delay > delay:
                        min_delay = delay
    return min_delay



def manathan_distance(position):
    return sum(abs(item) for item in position)


def _is_vertical(start, end):
    return start[0] == end[0]


def _is_horizontal(start, end):
    return start[1] == end[1]


def get_intersection(start_a, end_a, start_b, end_b):
    # line a is vertical
    if _is_vertical(start_a, end_a) and _is_horizontal(start_b, end_b):
        x_a = start_a[0]
        y_a_min = min(start_a[1], end_a[1])
        y_a_max = max(start_a[1], end_a[1])

        y_b = start_b[1]
        x_b_min = min(start_b[0], end_b[0])
        x_b_max = max(start_b[0], end_b[0])

        if x_b_min <= x_a <= x_b_max and y_a_min <= y_b <= y_a_max:
            return x_a, y_b

    elif _is_horizontal(start_a, end_a) and _is_vertical(start_b, end_b):
        return get_intersection(start_b, end_b, start_a, end_a)

    return None


# Tests

def test_convert_to_positions():
    directions = [('R', 3), ('U', 10), ('L', 2)]
    expected_positions = [
        (0, 0),
        (3, 0),
        (3, 10),
        (1, 10)
    ]
    assert convert_to_positions(directions) == expected_positions


def test_get_intersection():
    assert get_intersection(
        start_a=(2, 2),
        end_a  =(2, 10),
        start_b=(-1, 4),
        end_b  =(4, 4)
    ) == (2, 4)

    assert get_intersection(
        start_a=(2, 2),
        end_a  =(2, 3),
        start_b=(-1, 4),
        end_b  =(4, 4)
    ) is None

    assert get_intersection(
        start_b=(2, 2),
        end_b  =(2, 10),
        start_a=(-1, 4),
        end_a  =(4, 4)
    ) == (2, 4)


def test_get_intersections():
    positions_a = [
        (0, 0),
        (0, 10),
        (-4, 10),
        (-4, -5)
    ]
    positions_b = [
        (0, 0),
        (-8, 0),
        (-8, -3),
        (1, -3)
    ]
    assert get_intersections(positions_a, positions_b) == {(0, 0), (-4, 0), (-4, -3)}


def test_get_delays():
    assert get_delays([(0, 0), (10, 0), (10, 20)]) == [0, 10, 30]


if __name__ == '__main__':
    with open('input.txt') as f:
        wires = [
            [(dir_number[0], int(dir_number[1:])) for dir_number in row.strip().split(',')]
            for row in f.readlines()
        ]
    positions_a = convert_to_positions(wires[0])
    positions_b = convert_to_positions(wires[1])

    intersections = get_intersections(positions_a, positions_b)
    min_dist = min(manathan_distance(intersection) for intersection in intersections if manathan_distance(intersection) > 0)
    print(f'min_dist: {min_dist}')

    min_delay = get_intersections_with_min_delay(positions_a, positions_b)
    print(f'min_delay: {min_delay}')

