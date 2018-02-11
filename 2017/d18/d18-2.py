#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advent of code: Day 18 - Part 2
@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d18")

with open("input.txt", "r") as f:
    input = f.read()


input="""set i 31
set a 1
mul p 17
mul a 2
add i -1
add a -1
jgz p 2
snd 4
snd a
set i 127
rcv a
rcv d
set p 316
mul p 8505
mod p a
rcv e"""


commands = input.split('\n')


def process_command(reg, command, self_queue, other_queue):
    """
    Process command.
    Return shift to find next command to be executed.
    """
    
    c = command.split(' ')
    t = c[0]
    r = c[1]
    
    if len(c)==3:
        value = get_value(reg, c[2])
    
    if t == 'set':
        reg[r] = value
    elif t == 'add':
        reg[r] = reg.get(r,0) + value
    elif t == 'mul':
        reg[r] = reg.get(r,0) * value
    elif t == 'mod':
        reg[r] = reg.get(r,0) % value
    elif t == 'jgz':
        if reg.get(r,0) > 0:
            return value
    elif t == 'snd':
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
send_cnt = 0

cnt = 0

while True:
    
    cnt += 1
    
    print pos_0, pos_1
    print commands[pos_0], commands[pos_1]
    
    
    n_0 = process_command(reg_0, commands[pos_0], queue_0, queue_1)
    n_1 = process_command(reg_1, commands[pos_1], queue_1, queue_0)
    
    print reg_0, reg_1
    print queue_0, queue_1
    
    if 'snd' in commands[pos_1]:
        send_cnt += 1
    pos_0 += n_0
    pos_1 += n_1
    
#    print pos_0, pos_1
    
#    if (pos_0 == 36 and pos_1 == 28):
#        print(reg_0)
#        print(reg_1)
    
    if ((n_0 == 0 and n_1 == 0) or 
        min(pos_0,pos_1) < 0 or 
        max(pos_0,pos_1) >= len(commands)):
        break





reg_0, reg_1 = dict(), dict()
reg_0['p'] = 0
reg_1['p'] = 1

queue_0, queue_1 = [], []
pos_0, pos_1 = 0, 0
send_cnt = 0

cnt = 0

pid = 0

while True:
    
    cnt += 1
    
    if pid == 0:
        n_0 = process_command(reg_0, commands[pos_0], queue_0, queue_1)
        pos_0 += n_0
    else:
        n_1 = process_command(reg_1, commands[pos_1], queue_1, queue_0)
        pos_1 += n_1
        if 'snd' in commands[pos_1]:
            send_cnt += 1
    
    if (pid==0 and n_0==0) or (pid==1 and n_1==0):
        pid = 1-pid
    
    if ((n_0 == 0 and n_1 == 0) or 
        min(pos_0,pos_1) < 0 or 
        max(pos_0,pos_1) >= len(commands)):
        break









    


