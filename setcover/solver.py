#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import os
import time
from collections import namedtuple
from colorit import *
import sys
sys.setrecursionlimit(30000)

import solve_actual

Set = namedtuple("Set", ['index', 'cost', 'items'])

solution_cost = None

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), list(map(int, parts[1:]))))

    solution = solve_actual.solve(set_count, item_count, sets)
        
    # calculate the cost of the solution
    global solution_cost
    obj = sum([s.cost*solution[s.index] for s in sets])
    solution_cost = obj
    print(color_back('SOLUTION VALUE ' + str(obj), 255, 205, 205))

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        #file_location = sys.argv[1].strip()
        #with open(file_location, 'r') as input_data_file:
        #    input_data = input_data_file.read()
        #print(solve_it(input_data))

        files = os.listdir('./data')
        files.sort()
        files.sort(key=len)

        easy_set = set(files[:8])
        coursera_set = {'sc_157_0', 'sc_330_0', 'sc_1000_11', 'sc_5000_1', 'sc_10000_5', 'sc_10000_2'}
        easy_set_cost = 0
        coursera_set_cost = 0

        k = list(easy_set | coursera_set)
        k.sort()
        k.sort(key=len)
        total_cost = 0
        t0 = time.time()

        for f in k: #files:
            with open('./data/' + f, 'r') as input_data_file:
                input_data = input_data_file.read()
            print('\n' + color_back('TESTCASE ' + f, 215, 255, 215))
            solve_it(input_data)
            if f in easy_set:
                easy_set_cost += solution_cost
            if f in coursera_set:
                coursera_set_cost += solution_cost
            total_cost += solution_cost
            print(color_back('TOTAL COST: ' + str(total_cost) + ', TIME UP TO NOW: ' + str(time.time()-t0), 255, 215, 255))
        print('\n' + color_back('COURSERA SET: ' + str(coursera_set_cost/100860), 215, 255, 255), coursera_set_cost)
        print(color_back('EASY SET: ' + str(easy_set_cost/241), 215, 255, 255), easy_set_cost)


    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')

