from collections import defaultdict


testing = False


def read_data():
    filename = f'puzzle07{'-test' if testing else ''}.in'
    start = None
    splitters = set()
    with open(filename, 'r') as f:
        for row, line in enumerate(f):
            for col, c in enumerate(line):
                if c == '^':
                    splitters.add((row, col))
                elif c == 'S':
                    start = (row, col)
        last_row = row
    return start, splitters, last_row


def shoot_beam(start, splitters, beams, last_row):
    start_r, c = start
    for r in range(start_r, last_row):
        pos = r, c
        if pos in beams:
            return None
        if pos in splitters:
            return {(r, c - 1), (r, c + 1)}
        beams.add(pos)
    return None


def count_splits():
    start, splitters, last_row = read_data()
    beams = set()
    count = 0
    queue = set((start,))
    while queue:
        beam_start = queue.pop()
        if (result := shoot_beam(beam_start, splitters, beams, last_row)):
            queue |= result
            count += 1
    return count


def shoot_quantum_beam(start, splitters, last_row):
    _, col = start
    tachyons = {col: 1}
    for row in range(1, last_row):
        new_tachyons = defaultdict(int)
        for col, count in tachyons.items():
            if (row, col) in splitters:
                new_tachyons[col - 1] += count
                new_tachyons[col + 1] += count
            else:
                new_tachyons[col] += count
        tachyons = new_tachyons
    return sum(tachyons.values()) 


def part_1():
    return count_splits()


def part_2():
    return shoot_quantum_beam(*read_data())
