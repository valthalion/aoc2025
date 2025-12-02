import re


invalid_re = re.compile(r'''(\d+)\1+''')


testing = False


def read_data():
    filename = f'puzzle02{'-test' if testing else ''}.in'
    with open(filename, 'r') as f:
        for id_range in next(f).strip().split(','):
            yield id_range.split('-')


def invalid_ids(start, end):
    n_start, n_end = len(start), len(end)
    low, high = int(start), int(end)

    if n_start % 2 == 1:
        first = 10 ** (n_start // 2)
    else:
        first = int(start[:n_start // 2])

    if n_end % 2 == 1:
        last = 10 ** (n_end // 2) - 1
    else:
        last = int(end[:n_end // 2])

    for half in range(first, last + 1):
        n = int(str(half) * 2)
        if low <= n <= high:
            yield n


def invalid_ids2(start, end):
    for n in range(int(start), int(end) + 1):
        if invalid_re.fullmatch(str(n)):
            yield n


def part_1():
    total = 0
    for id_range in read_data():
        total += sum(invalid_ids(*id_range))
    return total


def part_2():
    total = 0
    for id_range in read_data():
        total += sum(invalid_ids2(*id_range))
    return total    
