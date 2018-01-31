#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 01:56:57 2018

@author: em
"""

input = 329
step = input


# Part 1
l = [0]
pos = 0
for i in range(1, 2018):
    pos = (pos + step) % len(l)
    pos += 1
    l.insert(pos, i)

print(l[l.index(2017) + 1])


# Part 2
l = [0]
pos = 0
for i in range(1, 50 * 10**6 + 1):
    pos = (pos + step) % i
    pos += 1
    if pos == 1:
        l.insert(pos, i)

print(l[1])