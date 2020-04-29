import math
import random
import time
import viz

import numpy as np

from graph import Node
from pool import Pool

def cost(tour, distance_matrix):
    return distance_matrix[tour, np.roll(tour, -1)].sum()

def reverse_subseqs(global_pool, distance_matrix, timeout=1.0):
    t0 = time.time()
    step = 0
    while time.time()-t0 < timeout:
        sol = global_pool.get_random()
        a = random.randint(0, len(sol)-1)
        b = random.randint(a, len(sol)-1)
        sol[a:b] = sol[a:b][::-1]
        global_pool.push(sol, cost(sol, distance_matrix))
        step += 1
    return step, time.time() - t0

def nn_populate(timeout, graph, distance_matrix, global_pool):
    t0 = time.time()
    steps = 0
    while time.time() - t0 < timeout:
        start = random.choice(graph)
        tour = start.nn_tour()
        global_pool.push(tour, cost(tour, distance_matrix))
        steps += 1
    return steps, time.time() - t0

def solve(points):
    if len(points) <= 2000:
        global_pool = Pool(k=1)
        distance_matrix = np.sqrt(((np.expand_dims(points, 1) - np.expand_dims(points, 0))**2).sum(2))
        graph = Node.create_graph(points, distance_matrix)


        for v in range(1):
            print('Running NN_POPULATE')
            s, t = nn_populate(1, graph, distance_matrix, global_pool)
            print(f'\nGenerated {s} tours in {t} seconds ({s/t})')

            print('Running REVERSE_SUBSEQS')
            s, t = reverse_subseqs(global_pool, distance_matrix, timeout=6)
            print(f'\nPerformed {s} reversed ss in {t} seconds ({s/t})')

            global_pool.rebase()



        tour = global_pool.get_best()
        global_pool.print_stats()
        print(tour)
        #viz.plot(points, tour[1])
        return tour[1]
    else:
        #global_pool = Pool(k=16)
        #populate_nn(global_pool, points, timeout=1)
        #reverse_subseqs(global_pool, points, timeout=1)
        #best = global_pool.get_best()
        return range(len(points))