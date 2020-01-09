
with open('input.txt') as f:
    weights = [int(weight.strip()) for weight in f.readlines()]


def get_fuel(weight):
    return max(weight // 3 - 2, 0)


def get_fuel_part2(weight):
    total_fuel = 0
    while weight > 0:
        # Computing fuel for current weight
        weight = get_fuel(weight)
        total_fuel += weight
    return total_fuel

assert get_fuel(1969) == 654
assert get_fuel(100756) == 33583

assert get_fuel_part2(1969) == 966

total_fuel = sum(get_fuel(weight) for weight in weights)
total_fuel_part2 = sum(get_fuel_part2(weight) for weight in weights)

print(f"Total fuel: {total_fuel}")
print(f"Total fuel part 2: {total_fuel_part2}")
