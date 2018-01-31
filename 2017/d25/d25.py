#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advent of code
Day 25 - Part 1
"""

import os
import re
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d25")

with open("input.txt", "r") as f:
    input = f.read()
    
lines = input.split('\n')

state_pattern = re.compile(r'In state ([A-F]):')
write_pattern = re.compile(r'.*Write the value ([01])\.')
move_pattern = re.compile(r'.*Move one slot to the (\w+)\.')
next_pattern = re.compile(r'.*Continue with state ([A-F])\.')
value_pattern = re.compile(r'.*If the current value is ([01]):')
step_pattern = re.compile(r'.*Perform a diagnostic checksum after (\d+) steps\.')


def create_config(lines):
    '''
    Returns a tuple (d, steps)
    d: dictionary with all the needed information about the reaction 
        depending on state and pointed value.
    steps: number of step before checksum.
    '''
    d = {c: {i: {} for i in range(2)} for c in 'ABCDEF'}
    for line in lines:
        m = state_pattern.match(line)
        if m:
            current_state = m.group(1)
        m = value_pattern.match(line)
        
        if m:
            current_value = int(m.group(1))
            
        m = write_pattern.match(line)
        if m:
            d[current_state][current_value]['write'] = int(m.group(1))
        
        m = move_pattern.match(line)
        if m:
            if m.group(1)=='left':
                move=-1
            elif m.group(1)=='right':
                move=1
            else:
                raise ValueError('Incorrect move pattern')
            d[current_state][current_value]['move'] = move
            
        m = next_pattern.match(line)
        if m:
            d[current_state][current_value]['next'] = m.group(1)
            
        m = step_pattern.match(line)
        if m:
            steps = int(m.group(1))

    return (d, steps)


d, steps = create_config(lines)

    
assert(d['A'][1]['write']==0)
assert(d['E'][0]['move']==-1)
assert(d['C'][0]['next']=='B')


t = {} # tape
p = 0 # position
state = 'A'

for i in range(steps):
    value = t.get(p, 0)
    t[p] = d[state][value]['write']
    p += d[state][value]['move']
    state = d[state][value]['next']


print('Solution of part 1: {}'.format(sum(t.values())))
    
    



