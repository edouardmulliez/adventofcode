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


def find_different_child(tree, parent):
    children = tree[node]['children']
    weights = [get_tower_weight(tree, child) for child in tree[node]['children']]
    if len(set(weights)) <= 1:
        return None # balanced
    
    if len(set(weights)) > 2:
        raise ValueError('More than 2 subtowers different weights')
    if len(children) == 2:
        raise ValueError('Unbalanced with only two children')
    
    for child in children:
        if weights.count(tree[child]['tower_weight']) == 1:
            return child
    
    raise ValueError('Could not find a single different weight')
    

def get_parent(node):    
    for parent in tree.keys():
        if node in tree[parent]['children']:
            return parent
    return None
    
# Find the node to be modified: unbalanced, but children balanced
node = root
while find_different_child(tree, node) is not None:
    node = find_different_child(tree, node)
# Find parent node
parent = get_parent(node)
for child in tree[parent]['children']:
    if child != node:
        diff = tree[node]['tower_weight'] - tree[child]['tower_weight']
        break

correct_weight = tree[node]['weight'] - diff
print correct_weight


