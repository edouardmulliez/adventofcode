#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:58:27 2018

@author: em
"""


import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d04")

with open("input.txt", "r") as f:
    input = f.readlines()


# Part 1

def is_psw_valid(psw):
    words = [word.replace('\n','') for word in psw.split(' ')]
    
    count = dict()
    for word in words:
        if word in count.keys():
            count[word] += 1
        else:
            count[word] = 1

    if max(count.values()) <= 1:
        return True
    return False
    
assert(is_psw_valid('aa bb  aa\n') == False)
assert(is_psw_valid('aa bb  cc\n') == True)

print(sum([is_psw_valid(psw) for psw in input]))


# Part 2

def is_anagram(s1, s2):
    """
    Returns True if s2 is an anagram of s1
    """
    if (len(s1) != len(s2)):
        return False
    s1 = ''.join(sorted([c for c in s1]))
    s2 = ''.join(sorted([c for c in s2]))
    return(s1 == s2)

def is_psw_valid2(psw):
    words = [word.replace('\n','') for word in psw.split(' ')]
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if is_anagram(words[i], words[j]):
                return False            
    return True

assert(is_anagram('abruti', 'brutis') == False)
assert(is_anagram('abruti', 'brutia') == True)

assert(is_psw_valid2('abcde xyz ecdab') == False)
assert(is_psw_valid2('a ab abc abd abf abj') == True)

print(sum([is_psw_valid2(psw) for psw in input]))



