#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:16:03 2018

@author: em
"""

import numpy as np
import pandas as pd
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


def find_non_duplicated(df, columns=[0,1,2]):
    """
    Returns a boolean array with False for indices corresponding to duplicated rows in df.
    """
    df = df.set_index(columns)
    return ~df.index.duplicated(keep=False)


p = []
v = []
a = []

for line in lines:
    p_el, v_el, a_el = process_line(line)
    p.append(p_el)
    v.append(v_el)
    a.append(a_el)

p = pd.DataFrame(p)
v = pd.DataFrame(v)
a = pd.DataFrame(a)


# Remove particules colliding
for i in range(1000):
    idx = find_non_duplicated(p)
    p = p.iloc[idx,:]
    v = v.iloc[idx,:]
    a = a.iloc[idx,:]
    v += a
    p += v

print p.shape[0]
    

