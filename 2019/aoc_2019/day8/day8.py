from collections import Counter


def split_into_layers(digits, layer_length):

    assert len(digits) % layer_length == 0

    layers = []
    i = 0
    while i < len(digits):
        layer = digits[i: i+layer_length]
        layers.append(layer)
        i += layer_length

    return layers


TRANSPARENT = 2

def combine_pixels(digits):
    # Returns the first non-transparent pixel
    for digit in digits:
        if digit != TRANSPARENT:
            return digit
    return digit


def combine_layers(layers, layer_length):
    combined_layer = []

    for i in range(layer_length):
        pixel = combine_pixels([layer[i] for layer in layers])
        combined_layer.append(pixel)

    return combined_layer


def convert(digit):
    if digit == 1:
        return '.'
    else:
        return ' '

def print_layer(layer, width, heigth):
    for i in range(height):
        row = layer[(i * width) : ((i+1) * width)]
        print(''.join(convert(n) for n in row))



with open('aoc_2019/day8/input.txt') as f:
    digits = [int(n) for n in f.readline().strip()]

    width = 25
    height = 6
    layer_length = width * height
    layers = split_into_layers(digits, layer_length)

    ## PART I

    # Count digits for each layer
    counters = [Counter(layer) for layer in layers]
    # Get layer with fewest zeros
    zero_nbs = [counter[0] for counter in counters]
    min_zero_index = zero_nbs.index(min(zero_nbs))

    counter_min_zero = counters[min_zero_index]
    print(counter_min_zero[1] * counter_min_zero[2])

    ## PART II

    combined_layer = combine_layers(layers, layer_length)
    print_layer(combined_layer, width, height)

    # PASS: CYKBY





