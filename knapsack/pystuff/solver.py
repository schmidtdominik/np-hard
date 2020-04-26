#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from collections import namedtuple

import actual_solve

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

    value, taken = actual_solve.solve(capacity, items)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')


    ############# REMOVE THIS ON SUBMIT? ############

    files = os.listdir('data')
    sum_ = 0
    for file in files:
        print(file)
        if '1000' in file:
            continue
        with open('data/' + file, 'r') as input_data_file:
            input_data = input_data_file.read()
        sum_ += int(solve_it(input_data).splitlines()[0].split()[0])
    print('TOTAL PERF: ' + str(sum_/221508504))

    #################################################