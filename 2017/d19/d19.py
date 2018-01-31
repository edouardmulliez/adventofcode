#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 16:06:40 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d19")

with open("input.txt", "r") as f:
    input = f.read()

lines = input.split('\n')
grid = [line for line in lines if len(line) > 0]


directions = [[0,1], [0,-1], [1,0], [-1,0]]

def update_dir_pos(grid, p, d):
    """
    Update direction and position
    """
    if grid[p[0]][p[1]] == '+':
        # Update direction
        for d2 in directions:
            if d2 != [-i for i in d]:
                if grid[p[0]+d2[0]][p[1]+d2[1]] != ' ':
                    break
        d[:] = d2
    # Update position
    p[0] += d[0]
    p[1] += d[1]


# Part 12
d = [1,0]  # direction 
p = [0, grid[0].find('|')] # position
letters = []
while grid[p[0]][p[1]] != ' ':
    c = grid[p[0]][p[1]]
    if c not in ['-', '|', '+']:
        letters.append(c)
    update_dir_pos(grid, p, d)    
print(''.join(letters))


# Part 2
d = [1,0]  # direction 
p = [0, grid[0].find('|')] # position
cnt = 0
while grid[p[0]][p[1]] != ' ':
    cnt += 1
    update_dir_pos(grid, p, d)    
print(cnt)

    
    
    


