#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 00:35:27 2018

@author: em
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 00:27:58 2018

@author: em
"""



import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d16")

with open("input.txt", "r") as f:
    input = f.read()

orders = input.split(',')

s = [chr(ord('a')+i) for i in range(16)]

def spin(s,n):
    return s[-n:] + s[:-n]

def exchange(s, i, j):
    """
    Exchange characters at positions i and j in s.
    Modify s inplace.
    """
    s[i], s[j] = s[j], s[i]
    return s

def partner(s, a, b):
    """
    Exchange character a and b positions in s.
    Modify s inplace.
    """
    i , j = s.index(a), s.index(b)
    return exchange(s, i, j)


def process_order(s, order):
    """
    Return new string depending on order
    """    
    t = order[0]
    
    if t == 's':
        n = int(order[1:])
        return spin(s, n)
    elif t == 'x':
        ids = [int(i) for i in order[1:].split('/')]
        return exchange(s, ids[0], ids[1])
    elif t == 'p':
        c = order[1:].split('/')
        return partner(s, c[0], c[1])
    else:
        raise ValueError('Order does not begin with "s", "x" or "p"')
        
        
# Tests    
s = [chr(ord('a')+i) for i in range(16)]
assert(spin(s, 2) == list('opabcdefghijklmn'))
s = [chr(ord('a')+i) for i in range(16)]
assert(exchange(s, 2, 0) == list('cbadefghijklmnop'))
s = [chr(ord('a')+i) for i in range(16)]
assert(partner(s, 'd', 'b') == list('adcbefghijklmnop'))
s = [chr(ord('a')+i) for i in range(16)]
assert(process_order(s, 's15') == list('bcdefghijklmnopa'))
s = [chr(ord('a')+i) for i in range(16)]
assert(process_order(s, 'x3/0') == list('dbcaefghijklmnop'))
s = [chr(ord('a')+i) for i in range(16)]
assert(process_order(s, 'pd/b') == list('adcbefghijklmnop'))


## Part 1

s = [chr(ord('a')+i) for i in range(16)]
for order in orders:
    s = process_order(s, order)
print('Answer of part 1: {0}'.format(''.join(s)))


## Part 2
dance_nb = 10**9

# Find a period in the dance
s = [chr(ord('a')+i) for i in range(16)]
init_s = list(s)
for i in xrange(dance_nb):
    for order in orders:
        s = process_order(s, order)
    if (s == init_s):
        break
if i == dance_nb:
    print('No period found')
period = i + 1
dance_nb = dance_nb % period

s = [chr(ord('a')+i) for i in range(16)]
for i in range(dance_nb):
    for order in orders:
        s = process_order(s, order)
print('Answer of part 2: {0}'.format(''.join(s)))



