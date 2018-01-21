#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:17:09 2018

@author: em
"""


import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d02")

with open("input.txt", "r") as f:
    lines = f.readlines()

# Part 1

def process_line(line):
    numbers = [int(nb) for nb in line.split('\t')]
    return(max(numbers)-min(numbers))
    
print(sum([process_line(line) for line in lines]))


# Part 2

def process_line2(line):
    numbers = [int(nb) for nb in line.split('\t')]
    
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if (j != i) and (numbers[i] % numbers[j] == 0):
                return(numbers[i]/numbers[j])
    
    raise ValueError('No correct couple found.')
    

print(sum([process_line2(line) for line in lines]))