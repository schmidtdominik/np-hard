import math
import random
import time

from colorit import color_back

import viz

import numpy as np

from graph import Node
from pool import Pool

def cost(tour, distance_matrix):
    return distance_matrix[tour, np.roll(tour, -1)].sum()

def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def cost_wo_distancematrix(tour, points):
    obj = length(points[tour[-1]], points[tour[0]])
    for index in range(len(points)-1):
        obj += length(points[tour[index]], points[tour[index+1]])
    return obj


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

def switch_two(global_pool, distance_matrix, timeout=1.0):
    t0 = time.time()
    step = 0
    while time.time()-t0 < timeout:
        sol = global_pool.get_random()
        a = random.randint(0, len(sol)-1)
        b = random.randint(a, min(len(sol)-1, a+10))
        sol[a], sol[b] = sol[b], sol[a]
        global_pool.push(sol, cost(sol, distance_matrix))
        step += 1
    return step, time.time() - t0

def switch_two_slow(global_pool, points, timeout=1.0, distance_factor=10):
    t0 = time.time()
    step = 0
    while time.time()-t0 < timeout:
        sol = global_pool.get_random()
        a = random.randint(0, len(sol)-1)
        b = random.randint(a, min(len(sol)-1, a+distance_factor))
        sol[a], sol[b] = sol[b], sol[a]
        global_pool.push(sol, cost_wo_distancematrix(sol, points))
        step += 1
    return step, time.time() - t0

def nn_populate(timeout, graph, distance_matrix, global_pool):
    t0 = time.time()
    steps = 0
    while time.time() - t0 < timeout:
        start = random.choice(graph)
        tour = start.nn_tour(randomized=False, rfactor=0.999)
        global_pool.push(tour, cost(tour, distance_matrix))
        steps += 1
    return steps, time.time() - t0

def reverse_subseqs_slow(global_pool, points, timeout=1.0):
    t0 = time.time()
    step = 0
    while time.time()-t0 < timeout:
        sol = global_pool.get_random()
        a = random.randint(0, len(sol)-1)
        b = random.randint(a, len(sol)-1)
        sol[a:b] = sol[a:b][::-1]
        global_pool.push(sol, cost_wo_distancematrix(sol, points))
        step += 1
    return step, time.time() - t0

class BestManager:
    local_improvement = 1
    no_degradation = 2

    def __init__(self, policy=local_improvement):
        self.best_solution = None
        self.best_value = float('inf')
        self.policy = policy

    def push(self, tour, value):
        if self.policy == self.local_improvement and value < self.best_value:
            print(color_back('*', 100, 100, 255), end='')
            self.best_solution = tour
            self.best_value = value
        return self.best_solution

def populate_nn_basic(global_pool, points, timeout=1.0):
    print('NN POP')
    t0 = time.time()
    step = 0
    while time.time() - t0 < timeout:
        print('start run')
        visited = np.zeros((len(points)), dtype=np.bool)
        sol = []

        init = random.randint(0, len(points) - 1)
        visited[init] = True
        sol.append(init)

        for i in range(len(points) - 1):
            legal_indices = np.nonzero(np.invert(visited))[0]
            distances_ = ((points-points[i])**2).sum(axis=1)
            distances = distances_[legal_indices]
            selected_legal = np.argmin(distances)
            sel = legal_indices[selected_legal]
            visited[sel] = True
            sol.append(sel)
        global_pool.push(sol, cost_wo_distancematrix(sol, points))
        step += 1
        # global_pool.print_stats()
    return step, time.time()-t0

def solve(points):
    if len(points) <= 2000:
        global_bm = BestManager(policy=BestManager.local_improvement)
        distance_matrix = np.sqrt(((np.expand_dims(points, 1) - np.expand_dims(points, 0))**2).sum(2))
        graph = Node.create_graph(points, distance_matrix)
        distance_matrix = np.sqrt(((np.expand_dims(points, 1) - np.expand_dims(points, 0)) ** 2).sum(2))
        graph = Node.create_graph(points, distance_matrix)

        for i in range(3):
            global_pool = Pool(k=4)
            print(color_back('|', 255, 200, 100), end='')
            print('Running NN_POPULATE')
            s, t = nn_populate(0.05, graph, distance_matrix, global_pool)
            print(f'\nGenerated {s} tours in {t} seconds ({s / t})')

            t0 = time.time()
            while time.time() - t0 < 4:
                global_pool.print_acc_stats()
                print('\nREVERSE_SUBSEQS: ', end='')
                s, t = reverse_subseqs(global_pool, distance_matrix, timeout=0.5)
                #print(f'\nPerformed {s} reversed ss in {t} seconds ({s / t})')

                print('\nSWITCH_TWO: ', end='')
                s, t = switch_two(global_pool, distance_matrix, timeout=0.5)
                #print(f'\nPerformed {s} switchtwo in {t} seconds ({s / t})')
            viz.plot(points, global_pool.get_best()[1])
            global_bm.push(global_pool.get_best()[1], global_pool.get_best()[0])

        """t0 = time.time()
        while time.time() - t0 < 4: # randomized restarts
            print(color_back('*', 255, 200, 100), end='')
            start = random.choice(graph)
            bm = BestManager()
            tour = start.nn_tour(randomized=True, rfactor=0.05)
            tour = bm.push(tour, cost(tour, distance_matrix))

            t0_2opt = time.time()
            while time.time() - t0_2opt < 2:
                sol = tour.copy()
                a = random.randint(0, len(sol) - 1)
                b = random.randint(a, len(sol) - 1)
                sol[a:b] = sol[a:b][::-1]
                tour = bm.push(sol, cost(sol, distance_matrix))
            global_bm.push(tour, cost(tour, distance_matrix))"""

        best_tour = global_pool.get_best()[1]

        return best_tour
    else:
        global_pool = Pool(k=1)
        populate_nn_basic(global_pool, points, timeout=5)
        print('done')
        #viz.plot(points, global_pool.get_best()[1])
        #print('plotted!')

        for i in range(5):
            reverse_subseqs_slow(global_pool, points, timeout=0.5)
            s, t = switch_two_slow(global_pool, points, timeout=5, distance_factor=4000)
        best = global_pool.get_best()
        print('plotting..')
        viz.plot(points, best[1])
        print('done')
        return best[1]
