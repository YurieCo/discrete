#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    taken = [0]*len(items)
    value, taken = knapsack(items, capacity, taken, 0, 0)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def evaluate(items, taken):
    value = 0
    for item in items:
        value += item.value * taken[item.index]
    return value

def weight(items, taken):
    weight = 0
    for item in items:
        weight += item.weight * taken[item.index]
    return weight

import copy
def knapsack(items, capacity, taken, index, best):
    if index == len(items):
        return evaluate(items, taken), copy.copy(taken)
    
    dontTake = copy.copy(taken)
    dontTake[index] = 0
    v1, t1 = knapsack(items, capacity, dontTake, index + 1, best)
    
    take = copy.copy(taken)
    take[index] = 1
    if weight(items, take) <= capacity:
        value = evaluate(items, take)
        estimate = value + relaxation(items, index+1)
        if best < estimate:
            v2, t2 = knapsack(items, capacity, take, index + 1, v1)
    
            if v2 > v1:
                return v2, t2
            else:
                return v1, t1
        else:
            return v1, t1
    else:
        return v1, t1

def relaxation(items, j):
    return sum([item.value for item in items[j:]])

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

