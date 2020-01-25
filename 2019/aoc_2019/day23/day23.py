from collections import deque

from aoc_2019.day11.computer import IntCodeComputer

NAT_ADDRESS = 255


class Nat:
    def __init__(self):
        self.memory = ()

    def update_memory(self, x, y):
        self.memory = (x, y)


def add_outputs_to_queues(outputs, queues, nat):
    assert len(outputs) % 3 == 0
    i = 0
    while i < len(outputs):
        address, x, y = outputs[i:i+3]

        if address == NAT_ADDRESS:
            nat.update_memory(x, y)
        else:
            queues[address].extend([x, y])
        i += 3


def part_1(nb_computers):
    computers = [IntCodeComputer(numbers) for _ in range(nb_computers)]
    queues = [deque() for _ in range(nb_computers)]
    nat = Nat()

    # Send to each computer its address
    outputs = []
    for i, computer in enumerate(computers):
        outputs.extend(computer.execute([i]))
    add_outputs_to_queues(outputs, queues, nat)

    while not nat.memory:
        outputs = []
        for i, computer in enumerate(computers):
            try:
                input = queues[i].popleft()
            except IndexError:
                input = -1
            outputs.extend(computer.execute([input]))
        add_outputs_to_queues(outputs, queues, nat)

    x, y = nat.memory
    return y


def part_2(nb_computers):
    computers = [IntCodeComputer(numbers) for _ in range(nb_computers)]
    queues = [deque() for _ in range(nb_computers)]
    nat = Nat()

    # Send to each computer its address
    outputs = []
    for i, computer in enumerate(computers):
        outputs.extend(computer.execute([i]))
    add_outputs_to_queues(outputs, queues, nat)

    last_nat_y_value = None
    nb_idle = 0
    while True:
        outputs = []
        for i, computer in enumerate(computers):
            try:
                input = queues[i].popleft()
            except IndexError:
                input = -1
            outputs.extend(computer.execute([input]))
        add_outputs_to_queues(outputs, queues, nat)
        if all(len(q) == 0 for q in queues):
            nb_idle += 1
        else:
            nb_idle = 0

        if nb_idle == 10:
            x, y = nat.memory
            # Update last_nat_y_value
            if last_nat_y_value is not None and last_nat_y_value == y:
                return y
            last_nat_y_value = y

            # Send latest NAT packet to computer 0
            outputs = computers[0].execute([x, y])
            add_outputs_to_queues(outputs, queues, nat)


if __name__ == '__main__':
    with open('aoc_2019/day23/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    nb_computers = 50
    y = part_1(nb_computers)
    print(f'PART I - y = {y}')


    y = part_2(nb_computers)
    print(f'PART II - y = {y}')
