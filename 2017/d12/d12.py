#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 00:22:44 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d12")

with open("input.txt", "r") as f:
    input = f.read()
    
lines = input.split('\n')


groups = dict({0: 0})


line = lines[0]

def process_line(groups, line):
    in_out = line.split('<->')
    
    # Get linked elements
    nodes = [int(in_out[0])] + [int(n) for n in in_out[1].split(',')]
    ids = [groups[n] for n in nodes if n in groups.keys()]
    
    # Choose a new id for the group
    if len(ids)==0:
        new_id = max(groups.values()) + 1
    else:
        new_id = min(ids)
        
    # update groups
    for n in nodes:
        groups[n] = new_id
    for node, i in groups.iteritems():
        if i in ids:
            groups[node] = new_id


for line in lines:
    process_line(groups, line)
    

# Part 1
nb_0 = sum([1 for key, value in groups.iteritems() if value == 0])
print(nb_0)
    
# Part 2

print(len(set(groups.values())))
max(groups.values())
    
    