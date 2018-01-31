#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advent of code
Day 23 - Part 2
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d23")

with open("input.txt", "r") as f:
    input = f.read()
    
commands = input.split('\n')


def add_command(reg, command, f_name):
    """
    Add a function with name f_name in dictionary reg corresponding to string 
    command.
    """
    # https://stackoverflow.com/questions/6098073/creating-a-function-object-from-a-string    
    c = command.split(' ')
    t = c[0] # command type
    
    assert(t in ['set','sub','mul','jnz'])
        
    if t == 'set':
        f = """def {f_name}(reg):
            reg["{r}"] = {value}
            return 1
        """.format(f_name=f_name, r=c[1], value=c[2])
    elif t == 'sub':
        f = """def {f_name}(reg):
            reg["{r}"] -= {value}
            return 1
        """.format(f_name=f_name, r=c[1], value=c[2])
    elif t == 'mul':
        f = """def {f_name}(reg):
            reg["{r}"] = {r} * {value}
            return 1
        """.format(f_name=f_name, r=c[1], value=c[2])
    elif t == 'jnz':
        f = """def {f_name}(reg):
            if {r} != 0:
                return {value}
            return 1
        """.format(f_name=f_name, r=c[1], value=c[2])
    # Add function to dictionary reg
    exec f in reg
    

reg = dict(zip([chr(ord('a')+i) for i in range(8)],[0]*8))
for i in range(len(commands)):
    add_command(reg, commands[i], 'f'+str(i))


import time
start = time.time()

reg['a'] = 1
cnt = 0
p = 0
while (0 <= p < len(commands)):
    if 'mul' in commands[p]:
        cnt += 1
    p += reg['f'+str(p)](reg)

end = time.time()
print(end - start)


print('Solution of part 2: {0}'.format(reg['h']))




