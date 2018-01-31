#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advent of code
Day 24 - Part 2
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


def get_max_len_strength(el, b_ids, last_port):
    '''
    Returns a tuple (length,strength). It corresponds to the maximum lenghts of
    a bridge with the remaining elements (not in b_ids). If multiple bridge have
    same length, the max strength is chosen.
    '''
    remaining_ids = set(range(len(el)))-set(b_ids)
    l_max = 0
    s_max = 0
    for i in remaining_ids:
        if last_port in el[i]:
            last_port_new = el[i][1-el[i].index(last_port)]
            l,s = get_max_len_strength(el, b_ids+[i], last_port_new)
            l = l + 1
            s = s + sum(el[i])
            if (l>l_max) or (l==l_max and s>s_max):
                l_max = l
                s_max = s
    
    return (l_max, s_max)

el = get_elements(input)

max_l,max_s = get_max_len_strength(el, [], 0)
print(max_s)


