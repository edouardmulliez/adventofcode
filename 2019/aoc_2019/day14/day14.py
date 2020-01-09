from collections import defaultdict
import math


ORE = 'ORE'
FUEL = 'FUEL'


def process_line(line):
    inputs, output = line.split(' => ')
    output_quantity, output_id = output.strip().split(' ')
    inputs_quantities = []
    for input in inputs.split(', '):
        input_quantity, input_id = input.split(' ')
        inputs_quantities.append((input_id, int(input_quantity)))

    return output_id, int(output_quantity), inputs_quantities


def get_ore_nb(output_id, needed_quantity, reactions, stock=None):
    stock = stock or defaultdict(int)
    if output_id == ORE:
        return needed_quantity, stock

    # First use what is in stock
    to_remove_from_stock = min(needed_quantity, stock[output_id])
    stock[output_id] -= to_remove_from_stock
    needed_quantity -= to_remove_from_stock

    if needed_quantity == 0:
        return 0, stock

    # Then use reactions
    reaction_quantity, inputs_quantities = reactions[output_id]
    needed_reaction_nb = math.ceil(needed_quantity / reaction_quantity)

    total_ore = 0
    for input_id, input_quantity in inputs_quantities:
        ore, stock = get_ore_nb(input_id, input_quantity * needed_reaction_nb, reactions, stock)
        total_ore += ore

    produced_output = needed_reaction_nb * reaction_quantity
    stock[output_id] += produced_output - needed_quantity

    return total_ore, stock


def get_ore_nb_simple(fuel_quantity, reactions):
    return get_ore_nb(FUEL, fuel_quantity, reactions)[0]



def find_root(f, a, b, target):
    if b - a < 2:
        return (a, b)

    c = (b+a) // 2
    if target < f(c):
        return find_root(f, a, c, target)
    else:
        return find_root(f, c, b, target)





# Part II
ore_quantity = 1000000000000

quantities = {
    13312: 82892753,
    180697: 5586022,
    2210736: 460664
}
for ratio, fuel_produced in quantities.items():
    naive_method = ore_quantity / ratio
    print(f'naive_method: {naive_method} - fuel_produced: {fuel_produced}')


with open('aoc_2019/day14/input.txt') as f:
    lines = [line.strip() for line in f.readlines()]

    reactions = {}
    for line in lines:
        output_id, output_quantity, inputs_quantities = process_line(line)
        reactions[output_id] = (output_quantity, inputs_quantities)

    # Part I
    total_ore, stock = get_ore_nb(FUEL, 1, reactions)
    print(f'total_ore: {total_ore}')

    # Part II
    target_ore_quantity = 1000000000000
    naive_fuel = target_ore_quantity / total_ore
    print(f'naive_fuel: {naive_fuel}')

    a = 2 * 10**6
    b = 4 * 10**6
    a, b = find_root(lambda x: get_ore_nb_simple(x, reactions), a, b, target_ore_quantity)

    print(f'f({a}): {get_ore_nb_simple(a, reactions)}')
    print(f'f({b}): {get_ore_nb_simple(b, reactions)}')





