from enum import Enum

# new stack: "deal into new stack"  -> reverse cards
# "cut N"  -> put first N cards at the end of the deck
#          -> if N < 0, put the last N cards at the end
# "deal with increment N"  --> rolling index with increment N

class Operation(Enum):
    DEAL_NEW = 0
    CUT = 1
    DEAL_INCREMENT = 2


def parse(command: str):
    command = command.strip().lower()
    if command.startswith("cut"):
        n = int(command[4:])
        return Operation.CUT, n
    elif command.startswith("deal into new stack"):
        return Operation.DEAL_NEW, None
    elif command.startswith("deal with increment"):
        n = int(command[19:])
        return Operation.DEAL_INCREMENT, n
    else:
        raise ValueError(f"Cannot parse command: {command}")


def execute(cards, command: str):
    op, n = parse(command)
    if op == Operation.DEAL_NEW:
        return deal_new_stack(cards)
    elif op == Operation.CUT:
        return cut(cards, n)
    elif op == Operation.DEAL_INCREMENT:
        return deal_with_increment(cards, n)
    else:
        raise NotImplementedError(f"Operation {op} is not supported")


def deal_new_stack(cards):
    return list(reversed(cards))


# Definition remains correct for n < 0
def cut(cards, n):
    return cards[n:] + cards[:n]


def deal_with_increment(cards, n):
    nb_cards = len(cards)
    new_deck = [0 for _ in range(nb_cards)]
    new_deck_idx = 0
    for deck_idx in range(nb_cards):
        new_deck[new_deck_idx] = cards[deck_idx]
        new_deck_idx = (new_deck_idx + n) % nb_cards
    return new_deck


def find_cycle_length(cards, commands):
    inital_cards = list(cards)

    i = 0
    while True:
        if i % 10 == 0:
            print(f'shuffle {i}')
        for command in commands:
            cards = execute(cards, command)
        i += 1
        if cards == inital_cards:
            return i


def update_params(command: str, multiplier: int, constant: int, nb_cards):
    op, n = parse(command)
    if op == Operation.CUT:
        constant = (constant - n) % nb_cards
    elif op == Operation.DEAL_NEW:
        multiplier = -multiplier
        constant = (-constant - 1) % nb_cards
    elif op == Operation.DEAL_INCREMENT:
        constant = (constant * n) % nb_cards
        multiplier = multiplier * n
    else:
        raise ValueError(f"Operation {op} is not implemented.")
    return multiplier, constant


def part_1(nb_cards, commands, value_to_find):
    multiplier = 1
    constant = 0
    for command in commands:
        multiplier, constant = update_params(command, multiplier, constant, nb_cards)

    position = (multiplier * value_to_find + constant) % nb_cards
    return position


def part_2(nb_cards, commands, position, nb_shuffles):
    multiplier = 1
    constant = 0
    for command in commands:
        multiplier, constant = update_params(command, multiplier, constant, nb_cards)

    # Invert relation: y = m x + c [N]  <=>  (y-c) * modinv(m) = x [N]
    inv_multiplier = modinv(multiplier, nb_cards)
    inv_constant = (-inv_multiplier * constant) % nb_cards

    inv_repeat_multiplier, inv_repeat_constant = update_params_for_repeated_cycles(
        inv_multiplier,
        inv_constant,
        nb_cards,
        nb_shuffles
    )

    value = (inv_repeat_multiplier * position + inv_repeat_constant) % nb_cards
    return value


def update_params_for_repeated_cycles(multiplier, constant, nb_cards, times):
    if times == 1:
        final_multiplier = multiplier
        final_constant = constant
    elif times % 2 == 0:
        m, c = update_params_for_repeated_cycles(multiplier, constant, nb_cards, times // 2)
        final_multiplier = m ** 2
        final_constant = (m + 1) * c
    else:
        m, c = update_params_for_repeated_cycles(multiplier, constant, nb_cards, times - 1)
        final_multiplier = m * multiplier
        final_constant = multiplier * c + constant
    final_multiplier = final_multiplier % nb_cards
    final_constant = final_constant % nb_cards
    return final_multiplier, final_constant


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    a = a % m
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# Tests

def test_deal_with_increment():
    cards = list(range(10))
    new_deck = deal_with_increment(cards, 3)
    assert new_deck == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]


if __name__ == '__main__':
    with open('aoc_2019/day22/input.txt') as f:
        commands = [line.strip() for line in f.readlines() if len(line.strip()) > 0]

    # PART I
    nb_cards = 10007
    cards = list(range(nb_cards))

    for command in commands:
        cards = execute(cards, command)

    position = cards.index(2019)
    print(f'Position of card 2019: {position}')


    # PART II
    nb_cards = 119315717514047
    nb_shuffles = 101741582076661
    position = 2020

    value = part_2(nb_cards, commands, position, nb_shuffles)

    print(f"PART II. Card at position {position}: {value}")