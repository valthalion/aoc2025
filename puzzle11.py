import networkx as nx


testing = False


def read_data(test_n):
    test_suffix = f'-test{test_n}'
    filename = f'puzzle11{test_suffix if testing else ''}.in'
    graph = nx.DiGraph()
    with open(filename, 'r') as f:
        for line in f:
            orig, dests = line.strip().split(': ')
            graph.add_edges_from((orig, dest) for dest in dests.split())
    return graph


def num_paths(graph, source, dest, paths=None):
    if paths is None:
        paths = {source: 1}

    if dest not in paths:
        paths[dest] = sum(
            num_paths(graph, source, node, paths)
            for node in graph.predecessors(dest)
        )
    return paths[dest]


def part_1():
    graph = read_data(1)
    return sum(1 for _ in nx.all_simple_paths(graph, 'you', 'out'))


def part_2():
    # Checking the graph, there is no path dac -> fft, so all paths need to be
    # svr -> fft -> dac -> out
    # fft and dac are chokepoints
    # checked: no cycles -> it's a DAG
    graph = read_data(2)
    paths_svr_fft = num_paths(graph, 'svr', 'fft')
    paths_fft_dac = num_paths(graph, 'fft', 'dac')
    paths_dac_out = num_paths(graph, 'dac', 'out')
    return paths_svr_fft * paths_fft_dac * paths_dac_out
