#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 23:42:12 2018

@author: em
"""

start_a = 516
start_b = 190
f_a = 16807
f_b = 48271
div = 2147483647


# Part 1
rounds = 40 * 10**6

def get_next_value(n, factor, divider):
    return (n*factor) % divider

def get_bin_s(n):
    """
    get the last 16 digits of n in binary.
    """
    s = "{0:0>31b}".format(n)
    return s[-16:]

n_a = start_a
n_b = start_b

count = 0
for i in range(rounds):    
    n_a = get_next_value(n_a, f_a, div)
    n_b = get_next_value(n_b, f_b, div)

    if get_bin_s(n_a) == get_bin_s(n_b):
        count += 1

print "Judge's count for part 1: {0:d}".format(count)

# Part 2

rounds = 5 * 10**6
mul_a = 4
mul_b = 8

def get_next_multiple(n, factor, divider, mul):
    """
    Get next value being a multiple of mul
    """
    n = get_next_value(n, factor, divider)
    while (n % mul != 0):
        n = get_next_value(n, factor, divider)    
    return n        

n_a = start_a
n_b = start_b

count = 0
for i in range(rounds):    
    n_a = get_next_multiple(n_a, f_a, div, mul_a)
    n_b = get_next_multiple(n_b, f_b, div, mul_b)

    if get_bin_s(n_a) == get_bin_s(n_b):
        count += 1

print "Judge's count for part 2: {0:d}".format(count)







    
