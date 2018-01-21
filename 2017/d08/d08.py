#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:02:45 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d08")

with open("input.txt", "r") as f:
    lines = [line.replace('\n','') for line in f.readlines()]
    
    
def process_line(reg, line):
    """
    Modify dictionary reg with instructions contained in line
    """
    instructions = line.split(' if ')
    
    if check_condition(reg, instructions[1]):
        make_assignment(reg, instructions[0])


def check_condition(reg, condition):
    """
    Returns True if statement in condition is True
    """
    condition = condition.split(' ')
    key = condition[0]
    op = condition[1]
    value = int(condition[2])
    
    assert(op in ['<', '<=', '>', '>=', '==', '!='])
    
    a = 0
    if key in reg.keys():
        a = reg[key]
    if op == '<=':
        return (a <= value)
    if op == '<':
        return (a < value)
    if op == '==':
        return (a == value)
    if op == '>':
        return (a > value)
    if op == '>=':
        return (a >= value)
    if op == '!=':
        return (a != value)
    
    
def make_assignment(reg, assignment):
    assignment = assignment.split(' ')
    key = assignment[0]
    op = assignment[1]
    value = int(assignment[2])
    
    assert(op in ['inc', 'dec'])
    
    if key not in reg.keys():
        reg[key] = 0
    
    if op == 'inc':
        reg[key] += value
    if op == 'dec':
        reg[key] -= value
    

reg = dict()
for line in lines:
    process_line(reg, line)
    
max_value = max(reg.values())





