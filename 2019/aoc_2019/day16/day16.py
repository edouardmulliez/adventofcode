import itertools
from functools import lru_cache
import numpy as np


BASE_PATTERN = [0, 1, 0, -1]


def get_mask_matrix(length, offset=0):
    matrix_length = length - offset
    matrix = np.zeros((matrix_length, matrix_length), dtype=int)
    for row in range(matrix_length):
        matrix[row, :] = get_mask_row(length, row, offset)
    return matrix


def get_mask_row(length, row, offset=0):
    pattern_with_offset = BASE_PATTERN[1:] + [0]

    mask_length = length - offset
    mask = np.zeros(mask_length, dtype=int)
    repeat = offset + row + 1
    col = row
    pattern_iterator = itertools.cycle(pattern_with_offset)
    while col < length:
        item = next(pattern_iterator)
        mask[col:col + repeat] = item
        col += repeat
    return mask


def compute_single_phase(inputs, mask_matrix=None):
    input_length = len(inputs)
    if mask_matrix is None:
        mask_matrix = get_mask_matrix(input_length)

    outputs = np.matmul(mask_matrix, inputs)
    outputs = np.mod(np.abs(outputs), 10)
    return outputs


# Idea: build a matrix. Only focus on the part necessary to compute the final result (lower right)
# N: offset for the output

# Other idea: since the offset > length // 2, there will be only 1 above the diagonal.
# This means that what we need to compute is close to a cumulative sum of the last elements.

# 1 1 1 1 1
#   1 1 1 1
#     1 1 1
#       1 1
#         1

def compute_single_phase_with_big_offset(inputs, total_length, offset):
    """
    inputs is a truncated input (already takes into account offset)
    """
    assert offset > total_length // 2 + 2

    inputs = np.array(inputs)
    reversed_inputs = np.flip(inputs)
    outputs = np.flip(np.cumsum(reversed_inputs))
    outputs = np.mod(np.abs(outputs), 10)
    return outputs


def compute_outputs(inputs, nb_phases):
    for i in range(nb_phases):
        # print(f'Phase {i}')
        inputs = compute_single_phase(inputs)
    return inputs


def compute_outputs_part2(inputs):
    NB_REPEAT_INPUT = 10000
    OUTPUT_OFFSET_LENGTH = 7
    offset = int(''.join(str(n) for n in inputs[:OUTPUT_OFFSET_LENGTH]))

    repeated_inputs = inputs * NB_REPEAT_INPUT
    total_length = len(repeated_inputs)

    inputs = repeated_inputs[offset:]
    for i in range(100):
        inputs = compute_single_phase_with_big_offset(inputs, total_length, offset)
    output = int(''.join(str(n) for n in inputs[:8]))
    return output



# TESTS

def test_compute_outputs():
    assert list(compute_outputs([1,2,3,4,5,6,7,8], 4)) == [0,1,0,2,9,4,9,8]
    assert list(compute_outputs([8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,8,6,4,5,5,9,5], 100)[:8]) == [2,4,1,7,6,1,7,6]
    assert list(compute_outputs([6,9,3,1,7,1,6,3,4,9,2,9,4,8,6,0,6,3,3,5,9,9,5,9,2,4,3,1,9,8,7,3], 100)[:8]) == [5,2,4,3,2,1,3,3]


def test_compute_single_phase():
    assert list(compute_single_phase([1,2,3,4,5,6,7,8])) == [4,8,2,2,6,1,5,8]


if __name__ == '__main__':
    with open('aoc_2019/day16/input.txt') as f:
        inputs = [int(n) for n in f.readline().strip()]

    # PART I
    outputs = compute_outputs(inputs, 100)
    result = "".join(str(n) for n in outputs[:8])
    print(f'result: {result}')

    # PART II
    output = compute_outputs_part2(inputs)
    print(f'part 2: {output}')
