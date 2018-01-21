#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 15:23:05 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d07")

with open("input.txt", "r") as f:
    lines = [line.replace('\n','') for line in f.readlines()]
    
    
# Part 1
    
def process_line(tree, line):
    """
    tree should be a dict. Add parent/children in line to tree.
    """
    elements = line.split('->')
    parent = elements[0].split(' ')[0]
    children = []
    if len(elements) == 2:
        children = elements[1].replace(' ','').split(',')
    tree[parent] = children

tree = dict()
for line in lines:
    process_line(tree, line)

all_children = [child for children in tree.values() for child in children ]
nodes = tree.keys()
root = [node for node in nodes if node not in all_children][0]

print(root)


# Part 2
line = lines[0]

def process_line2(tree, line):
    """
    tree should be a dict. Add parent/children in line to tree.
    """
    elements = line.split('->')
    parent = elements[0].split(' ')[0]
    weight = int(elements[0].split(' ')[1].replace('(','').replace(')',''))
    children = []
    if len(elements) == 2:
        children = elements[1].replace(' ','').split(',')
    tree[parent] = dict({'children': children, 'weight': weight})
    
    
def get_tower_weight(tree, node):
    """
    Get the weight of a given subtower (identified by key of base node)
    Update tree with tower weight information.
    """
    children = tree[node]['children']
    
    if 'tower_weight' in tree[node].keys():
        return tree[node]['tower_weight']
    
    weight = tree[node]['weight']
    weight += sum([get_tower_weight(tree, child) for child in children])
    tree[node]['tower_weight'] = weight
    
    return weight
        

tree = dict()
for line in lines:
    process_line2(tree, line)

def get_corrected_weight(tree, node):
    
    children = tree[node]['children']
    if len(children) == 0:
        return None
    
    weights = [get_tower_weight(tree, child) for child in tree[node]['children']]
    if len(weights) > 2 and len(set(weights)) > 1:
        # Tower is unbalanced
        for w in weights:
            if weights.count(w) > 1:
                return w
        print node
        print weights
        raise ValueError('No corrected weight found')
    
    for child in children:
        corrected_w = get_corrected_weight(tree, child)
        if corrected_w is not None:
            return corrected_w
    
    return None


get_corrected_weight(tree, root)




tree



