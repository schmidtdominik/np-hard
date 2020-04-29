from typing import List

import numpy as np


class Node:

    def __init__(self, xy, index, graphref, distance_matrix):
        self.xy = xy
        self.index = index
        self.edges_to = []
        self.graphref = graphref
        self.distance_matrix = distance_matrix

    def nn_edges(self, points, max_edges=None):
        distances = self.distance_matrix[self.index]
        indices = np.argsort(distances)
        for j in range(len(indices) if max_edges is None else min(max_edges + 1, len(indices))):
            if self.graphref[indices[j]] is not self:
                self.edges_to.append(self.graphref[indices[j]])

    def nn_tour(self):
        for n in self.graphref:
            n.marked = False
        return self.nn_tour_rec()

    def nn_tour_rec(self):
        self.marked = True
        for n in self.edges_to:
            if not n.marked:
                return [self.index] + n.nn_tour_rec()
        return [self.index]

    @property
    def pseudodegree(self):
        return len(self.edges_to)

    @staticmethod
    def create_graph(points, distance_matrix, max_edges: int = None) -> List['Node']:
        graph = []
        for i in range(len(points)):
            graph.append(Node(points[i], i, graph, distance_matrix))
        for node in graph:
            node.nn_edges(points, max_edges=max_edges)
        return graph

    def __repr__(self):
        return f'<{self.index} → |{[j.index for j in self.edges_to[:4]]}..|={self.pseudodegree}>'

    #def nn(self):