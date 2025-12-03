from collections import defaultdict


testing = False


pack_size = None


def read_data():
    global pack_size
    filename = f'puzzle03{'-test' if testing else ''}.in'
    with open(filename, 'r') as f:
        for line in f:
            if pack_size is None:
                pack_size = len(line) - 1  # remove the trainling '\n'
            batteries = (int(n) for n in line.strip())
            pack = defaultdict(list)
            for idx, value in enumerate(batteries):
                pack[value].append(idx)
            yield pack


def filter_pack(pack, pred):
    new_pack = {}
    for n in pack:
        positions = [p for p in pack[n] if pred(p)]
        if positions:
            new_pack[n] = positions
    return new_pack


def max_joltage(pack, depth=2, acc=0):
    joltage = 10 * acc

    # Leave enough batteries to fulfill depth
    usable_pack = filter_pack(pack, lambda p: p <= pack_size - depth)
    n = max(usable_pack)    
    pos = usable_pack[n][0]
    joltage += n

    new_depth = depth - 1
    if new_depth == 0:
        return joltage

    remaining = filter_pack(pack, lambda p: p > pos)
    return max_joltage(remaining, depth=new_depth, acc=joltage)


def part_1():
    packs = read_data()
    return sum(max_joltage(pack) for pack in packs)


def part_2():
    packs = read_data()
    return sum(max_joltage(pack, depth=12) for pack in packs)
