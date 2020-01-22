from collections import defaultdict, deque

FREE = '.'
START = 'AA'
END = 'ZZ'

OUTER = 'OUTER'
INNER = 'INNER'


def get_gate_positions(map):
    nrow = len(map)
    ncol = len(map[0])

    gate_positions = defaultdict(list)

    # Get horizontal gates
    for i in range(nrow):
        for j in range(ncol - 1):
            gate_name = map[i][j:j+2]
            if gate_name.isalpha():
                if j > 0 and map[i][j-1] == FREE:
                    position = (i, j - 1)
                elif j+2 < ncol and map[i][j+2] == FREE:
                    position = (i, j + 2)
                else:
                    raise ValueError(f'Cannot find valid position for gate {gate_name}')
                gate_positions[gate_name].append(position)

    # Get vertical gates
    for j in range(ncol):
        for i in range(nrow - 1):
            gate_name = map[i][j] + map[i+1][j]
            if gate_name.isalpha():
                if i > 0 and map[i-1][j] == FREE:
                    position = (i - 1, j)
                elif i + 2 < nrow and map[i+2][j] == FREE:
                    position = (i + 2, j)
                else:
                    raise ValueError(f'Cannot find valid position for gate {gate_name}')
                gate_positions[gate_name].append(position)

    return gate_positions


def is_outer_position(position, nrow, ncol):
    return (
        position[0] < 3 or position[0] >= nrow - 3 or
        position[1] < 3 or position[1] >= ncol - 3
    )
    

def build_portals(gate_positions, nrow, ncol):
    portals = {}
    for gate, positions in gate_positions.items():
        if len(positions) == 2:
            if is_outer_position(positions[0], nrow, ncol):
                portals[positions[0]] = (positions[1], OUTER)
                portals[positions[1]] = (positions[0], INNER)
            else:
                portals[positions[0]] = (positions[1], INNER)   
                portals[positions[1]] = (positions[0], OUTER)   
    return portals


def get_neighbors(position, map, portals):
    """
    position contains row, col and level.
    """
    neighbors = []
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta in deltas:
        neighbor = (position[0] + delta[0], position[1] + delta[1], position[2])
        try:
            if map[neighbor[0]][neighbor[1]] == FREE:
                neighbors.append(neighbor)
        except IndexError:
            pass
    if position[:2] in portals:
        next_position, portal_type = portals[position[:2]]
        level = position[2]
        if portal_type == OUTER:
            next_level = level - 1
        else:
            next_level = level + 1
        if next_level >= 0:
            neighbor = (next_position[0], next_position[1], next_level)
            neighbors.append(neighbor)

    return neighbors


def find_shortest_distance(map):
    gate_positions = get_gate_positions(map)
    nrow = len(map)
    ncol = len(map[0])
    portals = build_portals(gate_positions, nrow, ncol)

    start = gate_positions[START][0]
    end   = gate_positions[END][0]
    start = (start[0], start[1], 0)
    end   = (end[0], end[1], 0)

    queue = deque([start])
    distances = {start: 0}

    while queue and end not in distances:
        node = queue.popleft()
        for neighbor in get_neighbors(node, map, portals):
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)

    return distances[end]


if __name__ == '__main__':
    with open('aoc_2019/day20/input.txt') as f:
        map = [line.replace('\n', '') for line in f.readlines()]

    ncol = len(map[0])
    for row in map:
        assert len(row) == ncol

    gate_positions = get_gate_positions(map)
    nrow = len(map)
    ncol = len(map[0])
    portals = build_portals(gate_positions, nrow, ncol)
    print(gate_positions)
    print(portals)

    distance = find_shortest_distance(map)
    print(f'distance: {distance}')
