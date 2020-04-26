#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import time

from tqdm import tqdm

import solve_actual
import os
import sys

sys.setrecursionlimit(6000)
sol = None
nodes_ = None
def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    solution = solve_actual.solve(node_count, edge_count, edges)
    global sol, nodes_
    sol = solution
    nodes_ = node_count

    # prepare the solution in the specified output format
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print('ON SELECTED:')
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))

        files = os.listdir('./data')
        files.sort()
        files.sort(key=len)
        sum_colors = 0
        n = 0
        avg_percentage = 0
        t0 = time()
        for i, f in tqdm(enumerate(files), miniters=1):
            print(f'\nON {f}: TIME UP TO NOW:', time()-t0, f'i={i} COLORS={sum_colors}')

            with open('data/' + f, 'r') as input_data_file:
                input_data = input_data_file.read()
            result = solve_it(input_data)
            sum_colors += max(sol)
            n += 1
            avg_percentage += max(sol)/nodes_
        avg_percentage /= n
        print('color rate:', avg_percentage, 'validation:', sum_colors/1700, 'colors:', sum_colors)
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

