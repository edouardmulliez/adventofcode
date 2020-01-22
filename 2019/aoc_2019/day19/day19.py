from aoc_2019.day11.computer import IntCodeComputer
import math

def to_char(n):
    if n == 0:
        return '.'
    elif n == 1:
        return '#'
    else:
        raise ValueError


def print_map(map):
    for row in map:
        print(''.join(to_char(n) for n in row))


def is_active(numbers, x, y):
    computer = IntCodeComputer(numbers)
    return computer.execute([x, y])[0]


def _find_x_min(numbers, y, a, b, check_bounds=True):
    if check_bounds:
        assert not is_active(numbers, a, y)
        assert is_active(numbers, b, y)

    if b - a <= 1:
        return b

    c = (b + a) // 2
    active = is_active(numbers, c, y)
    if active:
        return _find_x_min(numbers, y, a, c, False)
    else:
        return _find_x_min(numbers, y, c, b, False)


def _find_x_max(numbers, y, a, b, check_bounds=True):
    if check_bounds:
        assert is_active(numbers, a, y)
        assert not is_active(numbers, b, y)

    if b - a <= 1:
        return a

    c = (b + a) // 2
    active = is_active(numbers, c, y)
    if active:
        return _find_x_max(numbers, y, c, b, False)
    else:
        return _find_x_max(numbers, y, a, c, False)


def get_x_bounds(y):
    x_min = 634
    x_max = 784
    y_ref = 949

    middle_point = round((x_min + x_max) / 2 * y / y_ref)
    a = math.floor((x_min - 2) * y / y_ref)
    b = math.ceil((x_max + 1) * y / y_ref)
    return a, middle_point, b


def find_x_min(numbers, y):
    a, middle_point, b = get_x_bounds(y)
    return _find_x_min(numbers, y, a, middle_point)


def find_x_max(numbers, y):
    a, middle_point, b = get_x_bounds(y)
    return _find_x_max(numbers, y, middle_point, b)


def get_width_at_y(numbers, y):
    x_max1 = find_x_max(numbers, y)
    y2 = y + 100 - 1
    x_min2 = find_x_min(numbers, y2)
    width = x_max1 - x_min2 + 1
    return width - 100


def find_correct_y(numbers, a, b):
    print(f'a, b: {a}, {b}')

    width_a = get_width_at_y(numbers, a)
    width_b = get_width_at_y(numbers, b)

    if width_a == 0:
        return a
    elif width_b == 0:
        return b
    elif width_a > 0:
        return find_correct_y(numbers, max(0, a - 500), a)
    elif width_b < 0:
        return find_correct_y(numbers, b, b + 500)
    elif width_a < 0 < width_b:
        c = (a + b) // 2
        width_c = get_width_at_y(numbers, c)
        if width_c == 0:
            return c
        elif width_c < 0:
            return find_correct_y(numbers, c, b)
        else:
            return find_correct_y(numbers, a, c)





if __name__ == '__main__':
    with open('aoc_2019/day19/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    active_count = 0
    for y in range(50):
        row = []
        for x in range(50):
            computer = IntCodeComputer(numbers)
            active_count += computer.execute([x, y])[0]

    y = 49
    x_min = _find_x_min(numbers, y, 10, 37)
    x_max = _find_x_max(numbers, y, 37, 50)

    print(f'y: {y}: {x_min} - {x_max}')
    assert is_active(numbers, x_max, y)
    assert not is_active(numbers, x_max + 1, y)

    correct_y = find_correct_y(numbers, 50, 1500)
    print(correct_y)

    for delta in range(10):
        y = correct_y - delta
        width = get_width_at_y(numbers, y)
        print(f'y: {y} - width: {width}')
        if width == 0:
            corrected_y = y
    print(f'corrected_y: {corrected_y}')

    corrected_x = find_x_min(numbers, corrected_y + 100 - 1)

    print(f'result: {10000 * corrected_x + corrected_y}')

