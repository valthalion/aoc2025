testing = False


def read_data():
    filename = f'puzzle09{'-test' if testing else ''}.in'
    with open(filename, 'r') as f:
        return [tuple(int(n) for n in line.split(',')) for line in f]


def calculate_area(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def calculate_areas(points):
    for idx, p1 in enumerate(points[:-1]):
        for p2 in points[idx + 1:]:
            yield calculate_area(p1, p2), p1, p2


def is_inside(p1, p2, p):
    return p1[0] < p[0] < p2[0] and p1[1] < p[1] < p2[1]


def line(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2:  # vertical
        return {'type': 'vert', 'x': x1, 'ymin': min(y1, y2), 'ymax': max(y1, y2)}
    else:  # horizontal
        return {'type': 'hor', 'y': y1, 'xmin': min(x1, x2), 'xmax': max(x1, x2)}


def get_lines(points):
    n = len(points)
    return [line(points[idx], points[(idx + 1) % n]) for idx in range(n)]


def crosses(a, b, c, d, ln):
    if ln['type'] == 'hor':
        return a['y'] < ln['y'] < c['y'] and ln['xmax'] > d['x'] and ln['xmin'] < b['x']
    else:  # ln['type'] == 'vert'
        return d['x'] < ln['x'] < b['x'] and ln['ymax'] > a['y'] and ln['ymin'] < c['y']


def part_1():
    points = read_data()
    return max(calculate_areas(points))[0]


def part_2():
    points = read_data()
    rectangles = sorted(calculate_areas(points), reverse=True)
    lines = get_lines(points)
    for area, *rectangle in rectangles:
        xmin, xmax = min(rectangle[0][0], rectangle[1][0]), max(rectangle[0][0], rectangle[1][0])
        ymin, ymax = min(rectangle[0][1], rectangle[1][1]), max(rectangle[0][1], rectangle[1][1])
        a = {'type': 'hor', 'y': ymin, 'xmin': xmin, 'xmax': xmax}
        b = {'type': 'vert', 'x': xmax, 'ymin': ymin, 'ymax': ymax}
        c = {'type': 'hor', 'y': ymax, 'xmin': xmin, 'xmax': xmax}
        d = {'type': 'vert', 'x': xmin, 'ymin': ymin, 'ymax': ymax}
        if any(crosses(a, b, c, d, ln) for ln in lines):
            continue
        return area
    return None
