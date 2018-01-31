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
    
    
#with open("test2.txt", "r") as f:
#    input = f.read()


# Part 1

def clean_garbadge(s):
    """
    Remove garbadge. Suppose that '!' have already been cleaned.
    """
    idx = []
    i = 0
    while (i < len(s)):
        if s[i] == '<':
            # In garbadge
            start = i
            while s[i] != '>':
                if s[i] == '!':
                    # Ignore next character
                    i += 1
                i += 1
            stop = i
            idx += range(start, stop+1)
        i += 1

    idx = [i for i in range(len(s)) if i not in idx]
    return(''.join([s[i] for i in idx]))


def get_score(s, level):
    """
    Compute score. Assume garbadge has been removed.
    """
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



# Part 2

def count_garbadge(s):
    """
    Count non-cancelled characters in garbadge.
    """
    count = 0
    i = 0
    while (i < len(s)):
        if s[i] == '<':
            # In garbadge
            i += 1
            while s[i] != '>':
                if s[i] == '!':
                    # Ignore next character
                    i += 2
                else:
                    count += 1
                    i += 1
        i += 1
        
    return count


assert(count_garbadge('zlkdnn<>m,!e,f')== 0)
assert(count_garbadge('zlkdnn<>m,!<random characters>e,f')== 17)
assert(count_garbadge('zlkd<<<<>nn<>m,!e,f')== 3)
assert(count_garbadge('zlkdnn<>m,!e,<!!!>>f')== 0)
assert(count_garbadge('zlkdnn<>m,!e,f')== 0)
assert(count_garbadge('<{o"i!a,<{i<a>')== 10)

print count_garbadge(input)
