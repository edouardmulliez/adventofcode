#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 00:22:23 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d13")

with open("input.txt", "r") as f:
    input = f.read()

#input ="""0: 3
#1: 2
#4: 4
#6: 4"""
    
lines = input.split('\n')
config = []
for line in lines:
    el = [int(e) for e in line.split(':')]
    config.append((el[0], el[1]))
config = dict(config)

def is_on_top(range, t):
    period = (2*range) - 2
    if (t % period == 0):
        return True
    return False


# Part 1
severity = 0
for depth, range in config.iteritems():
    if is_on_top(range, depth):
        severity += depth * range
        
print(severity)


# Part 2

def is_caught(config, delay):
    for depth, range in config.iteritems():
        if is_on_top(range, depth + delay):
            return True
    return False

delay = 0
while is_caught(config, delay):
    delay += 1
    
print(delay)


