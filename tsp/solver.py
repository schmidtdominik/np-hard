#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import math
import os
import pickle
import time
from collections import namedtuple
from pathlib import Path

from colorit import color_back
from tqdm import tqdm
import numpy as np

import solve_actual
import sys
sys.setrecursionlimit(2000)
Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

global_cost = None

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points_np = []
    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
        points_np.append([float(parts[0]), float(parts[1])])
    points_np = np.array(points_np)
    solution = solve_actual.solve(points_np)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    global global_cost
    global_cost = obj

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))



    return output_data


import sys

reference_results = {'tsp_51_1': 435.44325409375847, 'tsp_100_3': 21375.867891721402, 'tsp_144_1': 60753.466323702385, 'tsp_200_2': 31187.555208128357, 'tsp_226_1': 83935.10965495049, 'tsp_493_1': 39029.17568677291, 'tsp_574_1': 43443.999183003376, 'tsp_1173_1': 69055.13542729376, 'tsp_1655_1': 73193.96704729644, 'tsp_1889_1': 377818.90061047144, 'tsp_33810_1': 229017808.0823745}

if __name__ == '__main__':
    files = os.listdir('./data')
    files.sort()
    files.sort(key=len)

    coursera_set = {'tsp_574_1'}#{'tsp_51_1', 'tsp_100_3', 'tsp_200_2', 'tsp_574_1', 'tsp_1889_1', 'tsp_33810_1'}
    other_set = set()#{'tsp_144_1', 'tsp_226_1', 'tsp_493_1', 'tsp_1173_1', 'tsp_1655_1'} # tsp_5_1
    results = {}

    todo = list(other_set | coursera_set)
    todo.sort()
    todo.sort(key=len)
    t0 = time.time()

    if not Path('stats.pickle').exists():
        stats = []
    else:
        with open('stats.pickle', 'rb') as f:
            stats = pickle.load(f)

    for file in todo:
        print(color_back(file, 215, 200, 255))
        with open('data/' + file, 'r') as f:
            input_data = f.read()
        solve_it(input_data)
        results[file] = global_cost
        print(color_back(file.upper() + '\t' + str(global_cost/reference_results[file]), 215, 255, 255))


    with open('./solve_actual.py') as f:
        hash_ = hashlib.md5(f.read().encode()).hexdigest()

    if not stats or stats[-1][0] != hash_:
        print('saved to stats')
        stats.append((hash_, results))
        with open('stats.pickle', 'wb+') as f:
            pickle.dump(stats, f)

    for f in todo:
        print(color_back(f.upper() + '\t' + str(results[f]/reference_results[f]), 215, 255, 255))
    print(sum(v for k, v in results.items() if k != 'tsp_33810_1')/sum(v for k, v in reference_results.items() if k != 'tsp_33810_1'), results)


