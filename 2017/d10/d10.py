#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 23:07:42 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d10")

with open("input.txt", "r") as f:
    input = f.read()
    
    
# Part 1
lengths = [int(nb) for nb in input.split(',')]


def reverse_from_pos(l, pos, length):
    """
    Will reverse the length elements in l, starting from pos.
    List is considered circular.
    """
    l = list(l) # Copy l    
    l_long = l + l
    l_short = l_long[pos:pos+length]
    l_reversed = list(reversed(l_short))
    
    if pos+length <= len(l):
        l[pos:pos+length] = l_reversed
    else:
        l[pos:] = l_reversed[0:len(l)-pos]
        l[0:length-len(l)+pos] = l_reversed[len(l)-pos:]
    
    return l

assert(reverse_from_pos(range(10), 8, 10) == [5, 4, 3, 2, 1, 0, 9, 8, 7, 6])

size = 256
l = range(size)
pos = 0
skip = 0

for length in lengths:
    l = reverse_from_pos(l, pos, length)
    pos = (pos + length + skip) % len(l)
    skip += 1

print(l[0]*l[1])


# Part 2

def xor_list(l):
    if len(l) < 2:
        raise ValueError('Length should be greater than 2')
    a = l[0]
    for el in l[1:]:
        a = a ^ el
    return a

assert(xor_list([65 , 27 , 9 , 1 , 4 , 3 , 40 , 50 , 91 , 7 , 6 , 0 , 2 , 5 , 68 , 22]) == 64)

def get_hash(s):
    """
    Compute dense hash for string s.
    """
    
    lengths = [ord(c) for c in s] # Convert to ASCII code
    suffix = [17, 31, 73, 47, 23]
    lengths += suffix
    round_nb = 64

    l = range(256)
    pos = 0
    skip = 0

    for r in range(round_nb):
        for length in lengths:
            l = reverse_from_pos(l, pos, length)
            pos = (pos + length + skip) % len(l)
            skip += 1

    # Get dense hash
    dense_hash = []
    for i in range(16):
        dense_hash.append(xor_list(l[16*i:16*(i+1)]))

    # Convert to hexa notation, with 2 hexadecimal digits
    dense_hash = ''.join([format(nb, '02x') for nb in dense_hash])
    
    return dense_hash


assert(get_hash('')=='a2582a3a0e66e6e86e3812dcb672a272')
assert(get_hash('AoC 2017')=='33efeb34ea91902bb2f59c9920caa6cd')
assert(get_hash('1,2,4')=='63960835bcdc130f0b66d7ff4f6a5a8e')
assert(get_hash('1,2,3')=='3efbe78a8d82f29979031a4aa0b16a9d')

get_hash(input)





