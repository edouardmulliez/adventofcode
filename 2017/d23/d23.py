#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advent of code
Day 23 - Part 1
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d23")

with open("input.txt", "r") as f:
    input = f.read()
    
commands = input.split('\n')


def process_command(reg, command):
    """
    Process command.
    Return shift to find next command to be executed.
    """    
    c = command.split(' ')
    t = c[0]
    r = c[1]

    assert(t in ['set','sub','mul','jnz'])
        
    if t == 'set':
        reg[r] = get_value(reg, c[2])
    elif t == 'sub':
        reg[r] -= get_value(reg, c[2])
    elif t == 'mul':
        reg[r] *= get_value(reg, c[2])
#    elif t == 'mod':
#        reg[r] = reg[r] % get_value(reg, c[2])
    elif t == 'jnz':
        if get_value(reg, c[1]) != 0:
            return get_value(reg, c[2])
    
    return 1


def get_value(reg, s):
    try:
        value = int(s)
    except ValueError:
        value = reg[s]
    return value


#d = {'a':7}
#exec "def f(x): return x + a" in d
#exec "def f2(x): return x - 2" in d



# Part 1
reg = dict(zip([chr(ord('a')+i) for i in range(8)],[0]*8))

cnt = 0
p = 0
while (0 <= p < len(commands)):
    if 'mul' in commands[p]:
        cnt += 1
    p += process_command(reg, commands[p])
print('Solution of part 1: {0}'.format(cnt))


# Part 2
reg = dict(zip([chr(ord('a')+i) for i in range(8)],[0]*8))
reg['a'] = 1
p = 0
while (0 <= p < len(commands)):
#    command = commands[p]
#    print p
#    print reg
#    print command    
    p += process_command(reg, commands[p])

print('Solution of part 1: {0}'.format(reg['h']))




