#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 02:34:14 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d18")

with open("input.txt", "r") as f:
    input = f.read()

commands = input.split('\n')


# Part 1

def process_command(reg, last_snd, command):
    """
    Process command.
    Return shift to find next command to be executed.
    """
    
    c = command.split(' ')
    t = c[0]
    r = c[1]
    
    if r not in reg.keys():
        reg[r] = 0
    
    if t == 'set':
        reg[r] = get_value(reg, c[2])
    elif t == 'add':
        reg[r] += get_value(reg, c[2])
    elif t == 'mul':
        reg[r] *= get_value(reg, c[2])
    elif t == 'mod':
        reg[r] = reg[r] % get_value(reg, c[2])
    
    elif t == 'snd':
        last_snd[0] = reg[r]

    elif t == 'jgz':
        if reg[r] > 0:
            return get_value(reg, c[2])
        
    return 1


def get_value(reg, s):
    try:
        value = int(s)
    except ValueError:
        value = reg.get(s, 0)
    return value


def get_rcv(reg, last_snd, command):
    """
    Check if rcv command. If True and X not 0, return last sound.
    Else, return None.
    """
    c = command.split(' ')
    t = c[0]
    r = c[1]
    
    if r not in reg.keys():
        reg[r] = 0
        
    if t == 'rcv' and reg[r] != 0:
        try:
            snd = last_snd[0]
        except KeyError:
            print "No sound palyed before. Returned 0."
            snd = 0
        return snd
    
    return None


reg = dict()
last_snd = [None]

pos = 0
while (0 <= pos < len(commands)):
    snd = get_rcv(reg, last_snd, commands[pos]) 
    if snd is not None:
        break
    pos += process_command(reg, last_snd, commands[pos])


# Part 2

def process_command(reg, command, self_queue, other_queue):
    """
    Process command.
    Return shift to find next command to be executed.
    """
    
    c = command.split(' ')
    t = c[0]
    r = c[1]
    
    if r not in reg.keys():
        reg[r] = 0
    if len(c)==3:
        value = get_value(reg, c[2])
    
    if t == 'set':
        reg[r] = value
    elif t == 'add':
        reg[r] += value
    elif t == 'mul':
        reg[r] *= value
    elif t == 'mod':
        reg[r] = reg[r] % value
    elif t == 'jgz':
        if reg[r] > 0:
            return value
    elif t == 'snd':
        pass
        other_queue.append(get_value(reg, c[1]))
    elif t == 'rcv':
        if len(self_queue) > 0:
            reg[r] = self_queue[0]
            self_queue.pop(0)
        else:
            return 0
        
    return 1


def get_value(reg, s):
    try:
        value = int(s)
    except ValueError:
        if s in reg.keys():
            value = reg[s]
        else:
            value = 0
     
    return value



reg_0, reg_1 = dict(), dict()
reg_0['p'] = 0
reg_1['p'] = 1

queue_0, queue_1 = [], []
pos_0, pos_1 = 0, 0
cnt = 0

while True:
    n_0 = process_command(reg_0, commands[pos_0], queue_0, queue_1)
    n_1 = process_command(reg_1, commands[pos_1], queue_1, queue_0)
    if 'snd' in commands[pos_1]:
        cnt += 1
    pos_0 += n_0
    pos_1 += n_1
    
    print pos_0, pos_1
    
    if n_0 == 0 and n_1 == 0:
        break
    


