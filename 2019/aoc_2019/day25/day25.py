from aoc_2019.day11.computer import IntCodeComputer

from enum import Enum
import itertools


class Operation(Enum):
    MOVE = 0
    TAKE = 1
    DROP = 2
    INV  = 3
    SAVE_COMMANDS = 4

M_NORMAL = '.'
M_UNEXPLORED = '_'
M_START = 's'
M_DROID = 'x'
M_PRESSURE = 'P'


DIRECTIONS = {'north', 'south', 'west', 'east'}

DELTAS = {
    'north': (-1,  0),
    'south': ( 1,  0),
    'west' : ( 0, -1),
    'east' : ( 0,  1)
}

def ascii_to_string(n):
    return str(chr(n))


def ascii_ints_to_tring(ascii_ints):
    return  ''.join(ascii_to_string(n) for n in ascii_ints)


def print_ascii_ints(ascii_ints):
    print(ascii_ints_to_tring(ascii_ints))


def convert_to_ascii_ints(s):
    return [ord(c) for c in s]


def parse_command(command: str):
    command = command.strip()
    if command in DIRECTIONS:
        return Operation.MOVE, command
    elif command.startswith("take") or command.startswith("drop"):
        obj = command.split(maxsplit=1)[1]
        op = Operation.TAKE if command.startswith("take") else Operation.DROP
        return op, obj
    elif command == "inv":
        return Operation.INV, None
    elif command == "SAVE":
        return Operation.SAVE_COMMANDS, None
    else:
        print()
        print(f"Warning: command {command} could not be parsed")
        print()
        return None, None


# Create a map of the successive positions of the droid.
# Also create a map of the objects. And the SASs.

def parse_prompt(s):
    next_directions = {d for d in DIRECTIONS if d in s}

    # get posible objects
    objects = []
    if "Items here:" in s:
        lines = [line.strip() for line in s.split('\n')]
        item_idx = lines.index("Items here:")
        item_idx += 1
        while item_idx < len(lines) and lines[item_idx].startswith('-'):
            obj = lines[item_idx][2:]
            objects.append(obj)
            item_idx += 1

    # is_pressure_sensitive
    is_pressure_sensitive = '== Pressure-Sensitive Floor ==' in s
    pressure_success = 'you are ejected back' not in s

    return next_directions, objects, is_pressure_sensitive, pressure_success



class Droid:
    def __init__(self, numbers):
        self.numbers = numbers
        self.computer = IntCodeComputer(self.numbers)
        self.position = (0, 0)
        self.map = {self.position: M_START}
        self.objects = {}
        self.inventory = set()
        self.commands = []
        self.execute('')

    def print_map(self):
        min_row = min(row for row, col in self.map)
        max_row = max(row for row, col in self.map)
        min_col = min(col for row, col in self.map)
        max_col = max(col for row, col in self.map)
        for i in range(min_row, max_row + 1):
            row = []
            for j in range(min_col, max_col + 1):
                try:
                    c = self.map[(i, j)]
                except KeyError:
                    c = ' '
                if (i, j) == self.position:
                    c = M_DROID
                row.append(c)
            print(''.join(row))


    def set_objects(self, objects):
        objects = set(objects)
        missing_objects = objects - self.inventory
        to_remove = self.inventory - objects
        for obj in missing_objects:
            command = f'take {obj}\n'
            self.execute(command)
        for obj in to_remove:
            command = f'drop {obj}\n'
            self.execute(command)

    def execute(self, command: str):
        print(f'Command: {command}')
        if command:
            assert command.endswith('\n')
            self.commands.append(command)
        inputs = convert_to_ascii_ints(command)
        outputs = self.computer.execute(inputs)
        output_s = ascii_ints_to_tring(outputs)
        print(output_s)

        # Update droid status
        if command:
            op, op_arg = parse_command(command)
            next_directions, objects, is_pressure_sensitive, pressure_success = parse_prompt(output_s)

            if op == Operation.SAVE_COMMANDS:
                with open('aoc_2019/day25/commands.txt', 'w') as f:
                    for command in self.commands:
                        f.write(command)

            elif op == Operation.MOVE:
                # Update position
                direction = op_arg
                delta = DELTAS[direction]
                next_position = (self.position[0] + delta[0], self.position[1] + delta[1])
                if is_pressure_sensitive:
                    self.map[next_position] = M_PRESSURE
                if not is_pressure_sensitive or pressure_success:
                    self.position = next_position

            # TODO: Also check the TAKE or DROP operation is valid
            elif op == Operation.TAKE:
                obj = op_arg
                self.inventory.add(obj)
            elif op == Operation.DROP:
                obj = op_arg
                self.inventory.remove(obj)

            # Update map
            if self.position not in self.map or self.map[self.position] == M_UNEXPLORED:
                self.map[self.position] = M_NORMAL

            if objects:
                for obj in objects:
                    self.objects[obj] = self.position

            # Flag unexplored positions
            if not is_pressure_sensitive or pressure_success:
                for direction in next_directions:
                    delta = DELTAS
                    delta = DELTAS[direction]
                    next_position = (self.position[0] + delta[0], self.position[1] + delta[1])
                    if next_position not in self.map:
                        self.map[next_position] = '_'

            # Print current state
            print()
            print("DROID STATE")
            self.print_map()
            print(f'inventory: {self.inventory}')

            return pressure_success


# Try combinations of objects until pressure is good

def find_correct_objects(droid):
    availables_objects = set(droid.inventory)
    for i in range(1, len(availables_objects) + 1):
        for objects in itertools.combinations(availables_objects, i):
            droid.set_objects(objects)
            pressure_success = droid.execute('south\n')
            if pressure_success:
                return droid.inventory


if __name__ == '__main__':
    with open('aoc_2019/day25/input.txt') as f:
        numbers = [int(n) for n in f.readline().strip().split(',')]

    droid = Droid(numbers)

    # Execute some commands on the droid
    with open('aoc_2019/day25/commands.txt') as f:
        commands = [line.strip() for line in f.readlines()]
    commands = [c for c in commands if c]
    commands = commands[:-2]
    print(commands)
    for command in commands:
        droid.execute(command + '\n')


    find_correct_objects(droid)

    # Successful inventory: {'fixed point', 'antenna', 'prime number', 'whirled peas'}
    # Code: 2622472

    while True:
        s = input("Type your command: ")
        s = s + '\n'

        droid.execute(s)



