testing = False


class Range:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __contains__(self, n):
        return self.low <= n <= self.high

    def __len__(self):
        return self.high - self.low + 1

    def __hash__(self):
        return self.low * int(1e15) + self.high

    def overlaps(self, other):
        return other.high >= self.low and other.low <= self.high

    def merge(self, other):
        self.low = min(self.low, other.low)
        self.high = max(self.high, other.high)


def read_data():
    filename = f'puzzle05{'-test' if testing else ''}.in'
    ranges = []
    with open(filename, 'r') as f:
        while (line := next(f).strip()):
            low, high = (int(n) for n in line.split('-'))
            ranges.append(Range(low, high))
        products = [int(line.strip()) for line in f]
    return ranges, products


def merge_ranges(ranges):
    merged = set()
    for r in ranges:
        if r in merged:
            continue
        overlaps = {other for other in merged if r.overlaps(other)}
        if overlaps:
            merged -= overlaps
            for other in overlaps:
                r.merge(other)
        merged.add(r)
    return merged


def part_1():
    ranges, products = read_data()

    def is_fresh(product):
        for r in ranges:
            if product in r:
                return True
        return False

    return sum(1 for product in products if is_fresh(product))


def part_2():
    ranges, _ = read_data()
    ranges = merge_ranges(ranges)
    return sum(len(r) for r in ranges)
