from collections import defaultdict


def create_graph(edges):
    nodes = set()
    neighbors = defaultdict(list)

    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
        neighbors[a].append(b)

    return nodes, neighbors


def get_heights(neighbors, current_node, heights=None):
    if heights is None:
        # root of the tree
        heights = {current_node: 0}

    for node in neighbors[current_node]:
        heights[node] = heights[current_node] + 1
        get_heights(neighbors, node, heights)

    return heights


def get_parents(neighbors, current_node, parents=None):
    if parents is None:
        # root of the tree
        parents = {current_node: []}

    for node in neighbors[current_node]:
        parents[node] = parents[current_node] + [current_node]
        get_parents(neighbors, node, parents)

    return parents


def get_orbit_nb(nodes, neighbors):
    ROOT_NODE = 'COM'
    assert ROOT_NODE in nodes

    heights = get_heights(neighbors, ROOT_NODE)
    return sum(heights[node] for node in nodes)


def get_transfer_nb(neighbors):
    ROOT_NODE = 'COM'
    YOU = 'YOU'
    SAN = 'SAN'

    parents = get_parents(neighbors, ROOT_NODE)
    parents_you = parents[YOU]
    parents_san = parents[SAN]
    common_parents = set(parents_you).intersection(set(parents_san))

    return len(parents_san) + len(parents_you) - 2 * len(common_parents)


if __name__ == '__main__':
    with open('2019/day6/input.txt') as f:
        edges = [line.strip().split(')') for line in f.readlines()]

        nodes, neighbors = create_graph(edges)
        orbit_nb = get_orbit_nb(nodes, neighbors)
        print(f'orbit_nb: {orbit_nb}')

        transfer_nb = get_transfer_nb(neighbors)
        print(f'transfer_nb: {transfer_nb}')

