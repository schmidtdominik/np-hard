from typing import List


class Node:
    edges: List['Node']

    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.c = None
        self.degree = 0

    def edge_to(self, node: 'Node'):
        if not node in self.edges:
            self.edges.append(node)
            self.degree += 1

    def __repr__(self):
        return f'<{self.c}: {self.id} → {[j.id for j in self.edges]}>'

    def dfs_greedy_color(self):
        adj_colors = {n.c for n in self.edges if n.c is not None}
        if not adj_colors:
            self.c = 0
        else:
            for i in range(max(adj_colors)+2):
                if i not in adj_colors:
                    self.c = i
                    break
        # for n in sorted(self.edges, key=lambda x: -x.degree - sum(1 for n in x.edges if n.c is not None)):
        for n in sorted(self.edges, key=lambda x: -x.degree):
            if n.c is None:
                n.dfs_greedy_color()


def create_graph(node_count, edge_count, edges) -> List[Node]:
    graph: List[Node] = []
    for i in range(node_count):
        graph.append(Node(i))
    for edge in edges:
        graph[edge[0]].edge_to(graph[edge[1]])
        graph[edge[1]].edge_to(graph[edge[0]])
    return graph