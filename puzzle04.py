testing = False


def read_data():
    filename = f'puzzle04{'-test' if testing else ''}.in'
    rolls = {}

    def neighbours(r, c):
        neighbour_pos = ((r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1))
        return set(pos for pos in neighbour_pos if pos in rolls)

    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, pos in enumerate(line.strip()):
                if pos == '@':
                    ns = neighbours(r, c)
                    rolls[(r, c)] = ns
                    for rr, cc in ns:
                        rolls[(rr, cc)].add((r, c))
    return rolls


def accessible(rolls):
    return tuple(roll for roll in rolls if len(rolls[roll]) < 4)


def remove(roll, rolls):
    for neighbour in rolls[roll]:
        rolls[neighbour].remove(roll)
    del rolls[roll]


def part_1():
    return len(accessible(read_data()))


def part_2():
    rolls = read_data()
    removed = 0
    while (to_remove := accessible(rolls)):
        for roll in to_remove:
            remove(roll, rolls)
        removed += len(to_remove)
    return removed
