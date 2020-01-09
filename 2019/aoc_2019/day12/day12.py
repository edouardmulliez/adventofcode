from collections import namedtuple


Point = namedtuple('Point', ['x', 'y', 'z'])
NB_COORDS = 3

# Part I

def update_velocities(positions, speeds):
    """
    speeds is updated inplace.
    """
    nb_moons = len(positions)
    for i in range(nb_moons):
        for j in range(nb_moons):
            # Update speed of moon i
            moon_i = positions[i]
            moon_j = positions[j]
            delta_speed = [0, 0, 0]
            for coord in range(NB_COORDS):
                if moon_j[coord] - moon_i[coord] > 0:
                    delta_speed[coord] = 1
                elif moon_j[coord] - moon_i[coord] < 0:
                    delta_speed[coord] = -1
            speeds[i] = Point(*[speeds[i][coord] + delta_speed[coord] for coord in range(NB_COORDS)])


def update_positions(positions, speeds):
    """
    positions is updated in place
    """
    nb_moons = len(positions)
    for i in range(nb_moons):
        speed = speeds[i]
        positions[i] = Point(*[positions[i][coord] + speed[coord] for coord in range(NB_COORDS)])


def compute_energy(positions, speeds):
    total_energy = 0
    for i in range(len(positions)):
        position = positions[i]
        speed = speeds[i]
        pot = sum(abs(item) for item in position)
        kin = sum(abs(item) for item in speed)
        energy = pot * kin
        total_energy += energy
    return total_energy


def part1(positions, nb_steps):
    nb_moons = len(positions)
    speeds = [Point(0,0,0) for _ in range(nb_moons)]

    for i in range(nb_steps):
        update_velocities(positions, speeds)
        update_positions(positions, speeds)

    total_energy = compute_energy(positions, speeds)
    return total_energy


def convert_line_to_point(line):
    coordinates = line.strip()[1:-1].split(', ')
    coordinates = Point(*[int(coord.split('=')[1]) for coord in coordinates])
    return coordinates


# Part II
# Each coordinate (x, y, z) behaves independently from the others. The idea is here to model only a
# single coordinate at a time, to know the cycle length for that particular coordinate.

def update_state_1d(positions, speeds):
    """
    positions and speeds are lists of ints (1d coordinates)
    """
    nb_moons = len(positions)

    # Update speeds
    for i in range(nb_moons):
        for j in range(nb_moons):
            # Update speed of moon i
            if positions[j] - positions[i] > 0:
                speeds[i] += 1
            elif positions[j] - positions[i] < 0:
                speeds[i] -= 1

    # Update positions
    for i in range(nb_moons):
        positions[i] += speeds[i]


def get_cycle_length_1d(positions, speeds):
    """
    positions and speeds are lists of ints (1d coordinates)
    """
    initial_positions = positions.copy()
    initial_speeds = speeds.copy()
    cycle_length = 0
    while True:
        update_state_1d(positions, speeds)
        cycle_length += 1
        if positions == initial_positions and speeds == initial_speeds:
            return cycle_length


def get_cycle_length(positions, speeds):
    """
    positions and speeds are list of 3d points
    """
    cycle_lengths = []
    for coord in range(NB_COORDS):
        positions_1d = [position[coord] for position in positions]
        speeds_1d = [speed[coord] for speed in speeds]
        cycle_length = get_cycle_length_1d(positions_1d, speeds_1d)
        cycle_lengths.append(cycle_length)
    return ppcm(*cycle_lengths)


def pgcd(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


def _ppcm(a, b):
    if a == 0 or b == 0:
        return 0
    else:
        return (a * b) // pgcd(a, b)


def ppcm(a, b, *others):
    res = _ppcm(a, b)
    if not others:
        return res
    else:
        return ppcm(res, others[0], *others[1:])


def part2(positions):
    nb_moons = len(positions)
    speeds = [Point(0,0,0) for _ in range(nb_moons)]
    cycle_length = get_cycle_length(positions, speeds)
    return cycle_length


# Tests

def test_convert_line_to_point():
    line = '<x=-16, y=15, z=-9>\n'
    assert convert_line_to_point(line) == Point(-16, 15, -9)


def test_ppcm():
    assert ppcm(2, 2, 3, 4) == 12


test_ppcm()


with open('aoc_2019/day12/input.txt') as f:
    positions = [convert_line_to_point(line) for line in f.readlines()]

    nb_steps = 1000
    total_energy = part1(positions.copy(), nb_steps)
    print(f'total_energy: {total_energy}')

    cycle_length = part2(positions)
    print(f'cycle_length: {cycle_length}')



