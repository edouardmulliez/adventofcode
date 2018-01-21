#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 14:34:57 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d06")

with open("input.txt", "r") as f:
    state = [int(nb) for nb in f.read().split('\t')]
    

# Part 1
    
def get_next_state(state):
    state = list(state) # copy list 
    pos = state.index(max(state))
    remaining = state[pos]
    state[pos] = 0
    
    while (remaining > 0):
        pos = (pos+1)%len(state)
        state[pos] += 1
        remaining -= 1
    
    return state


def get_step_nb(state):
    step = 0
    l = []
    while state not in l:
        l.append(state)
        state = get_next_state(state)
        step += 1
    return step


assert(get_step_nb([0,2,7,0]) == 5)

print("Result of part 1:")
print(get_step_nb(state))


# Part 2

def get_loop_size(state):    
    step = 0
    l = []
    while state not in l:
        l.append(state)
        state = get_next_state(state)
        step += 1
        
    return(step - l.index(state))


assert(get_loop_size([0,2,7,0]) == 4)

print("Result of part 2:")
print(get_loop_size(state))
