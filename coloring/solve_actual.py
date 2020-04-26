from random import random
from time import time

import numpy as np

from graph import create_graph
from colorit import *


#print(color_back("GURP", 255, 0, 0))

class Solver:

    def __init__(self, node_count, edge_count, edges):
        self.node_count = node_count
        self.edge_count = edge_count
        self.edges_as_given = edges
        self.graph = create_graph(node_count, edge_count, edges)

        #degrees = np.array([n.degree for n in self.graph])
        degrees = np.array([sum([j.degree for j in n.edges])+n.degree for n in self.graph])

        self.perm = np.argsort(degrees)[::-1]

        for i in range(len(self.perm)):
            self.graph[self.perm[i]].id = i

        self.edges_A = []
        self.edges_B = []
        for n in self.graph:
            for nb in n.edges:
                self.edges_A.append(n.id)
                self.edges_B.append(nb.id)

        self.edges_A = np.array(self.edges_A)
        self.edges_B = np.array(self.edges_B)

    def solve(self, timeout=None):
        self.timeout = timeout
        self.solve_start = time()

        dfs_graph = create_graph(self.node_count, self.edge_count, self.edges_as_given)
        for n in dfs_graph:
            if n.c is None:
                n.dfs_greedy_color()
        dfs_solution = [n.c for n in dfs_graph]
        dfs_solution_size = max([n.c for n in dfs_graph]) + 1
        #print(color_front('DFS LOWER BOUND: ' + str(max([n.c for n in dfs_graph]) + 1), 150, 20, 20))

        self.best_global_solution = None
        self.best_global_size = float('inf')

        colors = np.full(self.node_count, -1)
        filled = np.zeros_like(colors, dtype=np.bool)
        #free_neighbors = np.zeros_like(colors)
        #for i in self.edges_A:
        #    free_neighbors[i] += 1
        #for i in self.edges_B:
        #    free_neighbors[i] += 1

        self.solve_rec(colors, filled)

        self.best_global_solution = self.best_global_solution[np.argsort(self.perm)]
        if self.best_global_solution is None or dfs_solution_size < self.best_global_size:
            return dfs_solution, dfs_solution_size
        return self.best_global_solution, self.best_global_size

    def solve_rec(self, colors, filled):
        if np.max(colors)+1 >= self.best_global_size or time()-self.solve_start > self.timeout:
            return None, float('inf')

        best_solution = None
        best_size = float('inf')

        """if np.sum(filled) > 6:
            if random() < 0.03:
                return None, float('inf')"""

        if np.sum(filled) == len(filled):
            if np.max(colors)+1 < self.best_global_size:
                #print('BEST GLOBAL:', np.max(colors)+1)
                self.best_global_size = np.max(colors)+1
                self.best_global_solution = colors
            return colors, np.max(colors)+1

        possible_candidate_nodes = np.arange(len(filled))[np.invert(filled)]
        #candidate_like = free_neighbors[np.invert(filled)]
        #candidate_nodes = possible_candidate_nodes[np.argsort(candidate_like)]
        next_filled = possible_candidate_nodes[0]
        #next_filled = candidate_nodes[0]

        """        if len(possible_candidate_nodes) >= 2:
                    neighborsA = np.concatenate([self.edges_B[np.argwhere(self.edges_A == possible_candidate_nodes[0])],
                                                self.edges_A[np.argwhere(self.edges_B == possible_candidate_nodes[0])]], axis=0).flatten()
                    neighborsB = np.concatenate([self.edges_B[np.argwhere(self.edges_A == possible_candidate_nodes[1])],
                                                 self.edges_A[np.argwhere(self.edges_B == possible_candidate_nodes[1])]], axis=0).flatten()
        
                    if sum(filled[neighborsA]) < sum(filled[neighborsB]):
                        next_filled = possible_candidate_nodes[1]
        """
        #if len(possible_candidate_nodes) >= 2 and random() < 0.1:
        #    next_filled = np.random.choice(possible_candidate_nodes)

        neighbors = np.concatenate([self.edges_B[np.argwhere(self.edges_A == next_filled)], self.edges_A[np.argwhere(self.edges_B == next_filled)]], axis=0).flatten()
        neighbor_colors = colors[neighbors]
        max_color = np.max(neighbor_colors)

        possible_colors = np.arange(max_color+2)
        #np.random.shuffle(possible_colors)
        for c in possible_colors:
            if c not in neighbor_colors:
                colors_new = colors.copy()
                filled_new = filled.copy()
                #free_neighbors_new = free_neighbors.copy()
                colors_new[next_filled] = c
                filled_new[next_filled] = True
                #free_neighbors_new[neighbors] -= 1
                solution, size = self.solve_rec(colors_new, filled_new)
                if size < best_size:
                    best_size = size
                    best_solution = solution

        return best_solution, best_size

def solve(node_count, edge_count, edges):
    solver = Solver(node_count, edge_count, edges)
    solution, size = solver.solve(timeout=6)
    #print('BEST:', size)
    return solution
