#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 17:35:49 2018

@author: em
"""

import numpy as np
import re
import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d20")

with open("input.txt", "r") as f:
    input = f.read()

lines = input.split('\n')

def process_line(line):
    """
    Get a position, speed and accelaration lists from line.
    Returns a tuple (p, v, a)
    """    
    values = re.split('<|>', line)
    values = [values[i] for i in [1,3,5]]
    values = [[int(nb) for nb in v.split(',')] for v in values]
    return tuple(values)

def find_closest(d, d_v, d_a):
    """
    Use distance, distance_speed, distance_accelaration to find particle 
    which will stay closest to zero in long-term.
    """
    
    id_a = np.argwhere(d_a == d_a.min()).flatten()
    id_v = np.argwhere(d_v == d_v.min()).flatten()
    id_p = np.argwhere(d == d.min()).flatten()
    
    min_id = set(id_a) & set(id_v) & set(id_p)
    if len(min_id)==1:
        return min_id.pop()
    else:
        return None
    

p = []
v = []
a = []

for line in lines:
    p_el, v_el, a_el = process_line(line)
    p.append(p_el)
    v.append(v_el)
    a.append(a_el)

p = np.array(p)
v = np.array(v)
a = np.array(a)



id_closest = None
while id_closest is None:
    distances = []
    for t in range(100):
        v += a
        p += v
        dist = np.absolute(p).sum(axis=1)
        distances.append(dist)
    distances = np.array(distances)
    distances_v = np.diff(distances, axis=0)
    distances_a = np.diff(distances_v, axis=0)
    id_closest = find_closest(distances[-1,:], distances_v[-1,:], distances_a[-1,:])


print id_closest




