testing = False


def read_data():
    filename = f'puzzle01{'-test' if testing else ''}.in'
    with open(filename, 'r') as f:
        for line in f:
            direction, n = line[0], int(line[1:])
            yield n if direction == 'R' else -n


def password(start, seq, count_all_clicks=False):
    current, count = start, 0
    for n in seq:
        start_from_zero = (current == 0)
        cycles, current = divmod(current + n, 100)
        if count_all_clicks:
            count += abs(cycles)
            if n < 0:
                if current == 0:
                    count += 1
                if start_from_zero:
                    count -= 1
        elif current == 0:
            count += 1
    return count


def part_1():
    return password(start=50, seq=read_data())


def part_2():
    return password(start=50, seq=read_data(), count_all_clicks=True)
