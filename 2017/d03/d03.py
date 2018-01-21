#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:36:03 2018

@author: em
"""

k = 361527


# Part 1

def get_dist(k):
    # Find in which square k is.
    n = 0
    s_n = 1    
    while (s_n < k):
        n += 1
        s_n += 8 * n    
    s_n -= 8*n
        
    dif = (k - s_n) % (2*n)
    if (dif < n):
        dist = 2*n-dif
    else:
        dist = dif
    return dist


assert(get_dist(26) == 5)
assert(get_dist(17) == 4)
assert(get_dist(14) == 3)


print(get_dist(k))


# Part 2

def get_next_ix(ix):
    """
    For a given position, give the position of the next number.
    """
    x = ix[0]
    y = ix[1]
           
    if x == 0 and y == 0:
        return(1,0)
    if (y > 0) and (y >= x) and (y > -x):
        return(x-1,y)
    if (x < 0) and (y <= -x) and (y > x):
        return(x,y-1)
    if (y < 0) and (y <= x) and (y <= -x):
        return(x+1,y)
    if (x > 0) and (y > -x) and (y < x):
        return(x,y+1)
    
    raise ValueError('Case not taken into account.')


assert(get_next_ix((-2,2)) == (-2,1))
assert(get_next_ix((2,1)) == (2,2))
assert(get_next_ix((-2,-1)) == (-2,-2))
assert(get_next_ix((-2,2)) == (-2,1))
assert(get_next_ix((2,2)) == (1,2))
assert(get_next_ix((2,0)) == (2,1))
assert(get_next_ix((0,2)) == (-1,2))
assert(get_next_ix((-2,0)) == (-2,-1))
assert(get_next_ix((0,-2)) == (1,-2))

d = dict({(0,0): 1})
last_ix = (0,0)

while (d[last_ix] < k):  
    last_ix = get_next_ix(last_ix)    
    neighbor_ix = []
    for ix in d.keys():
        if (abs(ix[0]-last_ix[0]) <= 1) and (abs(ix[1]-last_ix[1]) <= 1):
            neighbor_ix.append(ix)
    d[last_ix] = sum([d[ix] for ix in neighbor_ix])
        
assert(d[(-2,0)] == 330)
assert(d[(0,-2)] == 806)

print(d[last_ix])
    
    

    
    
    
    









