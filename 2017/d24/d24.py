#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advent of code
Day 24 - Part 1
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d24")

with open("input.txt", "r") as f:
    input = f.read()
    
def get_elements(input):
    elements = []
    for line in input.split('\n'):
        el = [int(nb) for nb in line.split('/')]
        elements.append(el)
    return elements

def get_max_strength(el, b_ids, last_port):
    '''
    Returns the max strenght for the end of a bridge beginning at last_port with 
    the remaining elements (not in b_ids).
    '''
    remaining_ids = set(range(len(el)))-set(b_ids)
    s_max = 0
    for i in remaining_ids:
        if last_port in el[i]:
            last_port_new = el[i][1-el[i].index(last_port)]
            s = sum(el[i]) + get_max_strength(el, b_ids+[i], last_port_new)
            s_max = max(s_max, s)
    
    return s_max

el = get_elements(input)

max_s = get_max_strength(el, [], 0)
print(max_s)
