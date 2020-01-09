from collections import Counter


def is_sorted(items):
    for i in range(len(items) - 1):
        if items[i + 1] < items[i]:
            return False
    return True

def has_2_adjacent_equal_digit(digits):
    for i in range(len(digits) - 1):
        if digits[i + 1] == digits[i]:
            return True
    return False


def has_digit_exactly_twice(digits):
    c = Counter(digits)
    return 2 in c.values()


def is_valid_password(number):
    digits = [int(i) for i in str(number)]

    if not is_sorted(digits):
        return False
    if not has_2_adjacent_equal_digit(digits):
        return False

    return True


def is_valid_password2(number):
    digits = [int(i) for i in str(number)]

    if not is_sorted(digits):
        return False
    if not has_2_adjacent_equal_digit(digits):
        return False
    if not has_digit_exactly_twice(digits):
        return False

    return True



assert is_valid_password(111111)
assert not is_valid_password(223450)
assert not is_valid_password(123789)


print(sum(is_valid_password(i) for i in range(136760, 595730 + 1)))
print(sum(is_valid_password2(i) for i in range(136760, 595730 + 1)))
