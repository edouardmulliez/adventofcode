#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:05:42 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d09")

with open("input.txt", "r") as f:
    input = f.read()
    
    
with open("test2.txt", "r") as f:
    input = f.read()


# Take care of ! character:
def clean_exclamation(s):
    """
    Remove characters depending on '!' positions.
    """
    idx = []
    for i in range(1,len(s)):
        if s[i] == '!' and s[i-1] != '!':
            idx += [i, i+1]
    idx = [i for i in range(len(s)) if i not in idx]
    
    return(''.join([s[i] for i in idx]))


def clean_garbadge(s):
    """
    Remove garbadge. Suppose that '!' have already been cleaned.
    """
    idx = []
    i = 0
    while (i < len(s)):
        if s[i] == '<':
            start = i
            while s[i] != '>':
                i += 1
            stop = i
            idx += range(start, stop+1)
        i += 1

    idx = [i for i in range(len(s)) if i not in idx]
    return(''.join([s[i] for i in idx]))


def get_score(s, level):
    if '{' not in s:
        return 0
    
    i = 0
    while i < len(s):
        if s[i] == '{':
            start = i
            count = 1
            while count != 0:
                i += 1
                if s[i] == '{':
                    count += 1
                if s[i] == '}':
                    count -= 1
            stop = i
            
            result = level + get_score(s[start+1:stop], level+1) 
            result += get_score(s[stop+1:], level)
            return(result)

        i += 1


def clean_and_score(s):
    s = clean_exclamation(s)
    s = clean_garbadge(s)
    return get_score(s, level=1)


assert(clean_and_score('{}') == 1)
assert(clean_and_score('{{{}}}') == 6)
assert(clean_and_score('{{},{}}') == 5)
assert(clean_and_score('{<a>,<a>,<a>,<a>}') == 1)
assert(clean_and_score('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9)
assert(clean_and_score('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9)
assert(clean_and_score('{{{},{},{{}}}}') == 16)
assert(clean_and_score('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3)

print(clean_and_score(input))

