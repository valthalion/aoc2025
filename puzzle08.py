from math import prod, sqrt
import networkx as nx


testing = False


def read_data():
    filename = f'puzzle08{'-test' if testing else ''}.in'
    with open(filename, 'r') as f:
        junctions = [tuple(int(n) for n in line.split(',')) for line in f]
    return junctions


def dist(a, b):
    return sqrt(sum((x - y)**2 for x, y in zip(a, b)))


def calc_distances(junctions):
    distances = [
        (dist(j1, j2), j1, j2)
        for idx, j1 in enumerate(junctions[:-1])
        for j2 in junctions[idx + 1:]
    ]
    distances.sort()
    return distances


def connect(junctions, distances, steps):
    graph = nx.Graph()
    graph.add_nodes_from(junctions)
    for idx in range(steps):
        d, j1, j2 = distances[idx]
        if nx.has_path(graph, j1, j2):
            continue
        graph.add_edge(j1, j2, weight=d)
    return graph


def connect_all(junctions, distances):
    graph = nx.Graph()
    graph.add_nodes_from(junctions)
    for d, j1, j2 in distances:
        if nx.has_path(graph, j1, j2):
            continue
        graph.add_edge(j1, j2, weight=d)
        if nx.is_connected(graph):
            return j1, j2
    return None


def part_1():
    junctions = read_data()
    distances = calc_distances(junctions)
    steps = 10 if testing else 1_000
    graph = connect(junctions, distances, steps)
    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    return prod(len(c) for c in components[:3])



def part_2():
    junctions = read_data()
    distances = calc_distances(junctions)
    j1, j2 = connect_all(junctions, distances)
    return j1[0] * j2[0]
