from math import prod


testing = False


def read_data():
    filename = f'puzzle06{'-test' if testing else ''}.in'
    n_rows = 3 if testing else 4
    with open(filename, 'r') as f:
        matrix = [[int(n) for n in next(f).strip().split()] for _ in range(n_rows)]
        ops = next(f).strip().split()
    return matrix, ops


def cephalopod_math(matrix):
    matrix_t = (''.join(line).strip() for line in zip(*matrix))
    new_matrix = []
    row = []
    for line in matrix_t:
        if line:
            row.append(int(line))
        else:
            new_matrix.append(row)
            row = []
    if row:
        new_matrix.append(row)
    return new_matrix


def read_data2():
    filename = f'puzzle06{'-test' if testing else ''}.in'
    n_rows = 3 if testing else 4
    with open(filename, 'r') as f:
        matrix = [next(f)[:-1] for _ in range(n_rows)]  # remove trailing '\n'
        ops = next(f).strip().split()
    return cephalopod_math(matrix), ops


def part_1():
    matrix, opcodes = read_data()
    matrix_t = zip(*matrix)
    ops = {'+': sum, '*': prod}
    return sum(ops[opcode](col) for opcode, col in zip(opcodes, matrix_t))


def part_2():
    matrix, opcodes = read_data2()
    ops = {'+': sum, '*': prod}
    return sum(ops[opcode](col) for opcode, col in zip(opcodes, matrix))
