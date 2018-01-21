#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 19:57:24 2018

@author: em
"""


import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d01")

with open("input.txt", "r") as f:
    s = f.read()



#%% Part One
    
def get_total(input):
    """
    Get input as string and compute total result.
    """
    numbers = [int(c) for c in input]
    numbers += numbers[0:1]
    total = 0
    for i in range(len(numbers)-1):
        if (numbers[i] == numbers[i+1]):
            total += numbers[i]
    return total

assert(get_total('112233')==6)
assert(get_total('1122331')==7)
assert(get_total('91212129')==9)


print "Result part 1:"
print(get_total(input))


#%% Part 2

def get_total2(s):
    numbers = [int(c) for c in s]
    shift = len(numbers)/2
    
    total = 0
    for i in range(len(numbers)):
        if (numbers[i] == numbers[(i+shift)%len(numbers)]):
            total += numbers[i]
    
    return(total)
    
assert(get_total2('123425') == 4)

print("Result part 2:")
print(get_total2(s))

    






