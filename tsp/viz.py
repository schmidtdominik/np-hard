import matplotlib.pyplot as plt
import numpy as np

def plot(points, tour):
    fig = plt.figure(figsize=(12, 12))
    plt.axis('equal')
    plt.suptitle('TSP tour')
    plt.scatter(points[:, 0], points[:, 1])
    start_node = tour[0]
    distance = 0.
    for i in range(len(tour)-1):
        start_pos = points[start_node]
        next_node = tour[i+1]
        end_pos = points[next_node]
        plt.annotate("",
                xy=start_pos, xycoords='data',
                xytext=end_pos, textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc3"))
        distance += np.linalg.norm(end_pos - start_pos)
        start_node = next_node

    plt.tight_layout()
    plt.show()