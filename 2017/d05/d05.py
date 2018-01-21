#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 14:19:45 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d05")

with open("input.txt", "r") as f:
    l = [int(nb) for nb in f.readlines()]

# Part 1

def get_step_nb(l):
    pos = 0
    step = 0
    l_len = len(l)
    while (0 <= pos < l_len):
        l[pos] += 1
        pos += l[pos] - 1
        step += 1
    return step

assert(get_step_nb([0,3,0,1,-3]) == 5)
print(get_step_nb(l))


# Part 2

def get_step_nb2(l):
    pos = 0
    step = 0
    l_len = len(l)
    while (0 <= pos < l_len):
        shift = l[pos]
        if shift >= 3:
            l[pos] -= 1
        else:
            l[pos] += 1
        pos += shift
        step += 1
    return step

assert(get_step_nb2([0,3,0,1,-3]) == 10)

print(get_step_nb2(l))
