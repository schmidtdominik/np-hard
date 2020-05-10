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

def dist_c(points, x, y):
    return np.sqrt(((points[x] - points[y]) ** 2).sum())

def switch_two_fastslow(global_pool, points, timeout=1.0, distance_factor=10):
    t0 = time.time()
    success_steps = 0
    total_steps = 0
    total_change = 0
    prev_cost, sol = global_pool.get_random_alt()
    while time.time()-t0 < timeout:
        a = random.randint(1, len(sol)-1)
        try:
            b = random.randint(a+4, min(len(sol)-2, a+distance_factor))
        except ValueError:
            continue

        cost_change = -dist_c(points, sol[a-1], sol[a]) - dist_c(points, sol[a], sol[a+1]) - dist_c(points, sol[b-1], sol[b]) - dist_c(points, sol[b], sol[b+1]) + \
                      dist_c(points, sol[a - 1], sol[b]) + dist_c(points, sol[b - 1], sol[a]) + dist_c(points, sol[a], sol[b+1]) + dist_c(points, sol[b], sol[a+1])

        if cost_change < 0:
            total_change += cost_change
            #print(color_back('*', 180, 180, 180), end='')
            sol[a], sol[b] = sol[b], sol[a]
            prev_cost += cost_change
            success_steps += 1
        total_steps += 1
    global_pool.push(sol, cost_wo_distancematrix(sol, points))#prev_cost

    print(f'performed {total_steps} switch_two_fastslow steps, with effectiveness {success_steps/total_steps} and total change {total_change}')

def nn_populate(timeout, graph, distance_matrix, global_pool, randomized=False, rfactor=0.999):
    t0 = time.time()
    steps = 0
    while time.time() - t0 < timeout:
        start = random.choice(graph)
        tour = start.nn_tour(randomized=randomized, rfactor=0.999)
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

def populate_nn_basic2(global_pool, points):
    visited = np.zeros((len(points)), dtype=np.bool)
    sol = []

    init = random.randint(0, len(points) - 1)
    visited[init] = True
    sol.append(init)

    for i in range(len(points) - 1):
        legal_indices = np.nonzero(np.invert(visited))[0]
        distances_ = np.sqrt(((points-points[sol[-1]])**2).sum(axis=1))
        selected_legal = np.argmin(distances_[legal_indices])
        sel = legal_indices[selected_legal]
        visited[sel] = True
        sol.append(sel)
    global_pool.push(sol, cost_wo_distancematrix(sol, points))

def solve(points):
    if len(points) <= 2000:
        global_bm = BestManager(policy=BestManager.local_improvement)
        distance_matrix = np.sqrt(((np.expand_dims(points, 1) - np.expand_dims(points, 0))**2).sum(2))
        graph = Node.create_graph(points, distance_matrix)

        for i in range(2):
            global_pool = Pool(k=16)
            print(color_back('|', 255, 200, 100), end='')
            print('Running NN_POPULATE')
            s, t = nn_populate(3, graph, distance_matrix, global_pool)
            print(f'\nGenerated {s} tours in {t} seconds ({s / t})')

            t0 = time.time()
            while time.time() - t0 < (200 if len(points) == 574 else 40):
                print(global_pool.get_best()[0])
                #global_pool.print_acc_stats()
                print('\nREVERSE_SUBSEQS: ', end='')
                s, t = reverse_subseqs(global_pool, distance_matrix, timeout=1)
                #print(f'\nPerformed {s} reversed ss in {t} seconds ({s / t})')

                print('\nSWITCH_TWO: ', end='')
                #s, t = switch_two(global_pool, distance_matrix, timeout=1)
                #print(f'\nPerformed {s} switchtwo in {t} seconds ({s / t})')
            #viz.plot(points, global_pool.get_best()[1])
            global_bm.push(global_pool.get_best()[1], global_pool.get_best()[0])

        return global_bm.best_solution
    else:
        global_pool = Pool(k=1)
        populate_nn_basic2(global_pool, points)
        print('done')
        #viz.plot(points, global_pool.get_best()[1])
        #print('plotted!')

        for i in range(0):
            #print('cycle')
            print('DEF COST1', cost_wo_distancematrix(global_pool.get_best()[1], points))
            reverse_subseqs_slow(global_pool, points, timeout=2)
            print('DEF COST2', cost_wo_distancematrix(global_pool.get_best()[1], points))
            print('s1')
            switch_two_fastslow(global_pool, points, timeout=6, distance_factor=100)
            print('s2')
            switch_two_fastslow(global_pool, points, timeout=4, distance_factor=1600)
            print('s3')
            switch_two_fastslow(global_pool, points, timeout=3, distance_factor=12000)
            print('s4')
        best = global_pool.get_best()
        #print('plotting..')
        viz.plot(points, best[1])
        #print('done')
        return best[1]
