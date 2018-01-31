#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 22:18:26 2018

@author: em
"""

import numpy as np

input = 'vbqugkhl'

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


def xor_list(l):
    if len(l) < 2:
        raise ValueError('Length should be greater than 2')
    a = l[0]
    for el in l[1:]:
        a = a ^ el
    return a


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

rows = []
for i in range(128):
    hash_input = input + '-' + str(i)
    h = get_hash(hash_input)
    rows.append("{0:0>128b}".format(int(h, 16)))

# Part 1
print(sum([1 for row in rows for c in row if c=='1']))


# Part 2

def get_neighbors(groups, x, y):
    n = []
    if x > 0:
        n.append(groups[x-1, y])
    if y > 0:
        n.append(groups[x, y-1])
    if x < groups.shape[0]-1:
        n.append(groups[x+1, y])
    if y < groups.shape[1]-1:
        n.append(groups[x, y+1])
    n = [i for i in n if i > 0]
    return n

grid = np.array([[int(c) for c in row] for row in rows])
groups = np.zeros((128,128), dtype=np.int)
    
for i in range(128):
    for j in range(128):
        if (grid[i, j] > 0):
            n = get_neighbors(groups,i,j)
            if len(n) == 0:
                groups[i,j] = groups.max() + 1
            else:
                value = min(n)
                groups[i,j] = value
                groups[np.isin(groups, n)] = value


len(np.unique(groups))-1





    
    