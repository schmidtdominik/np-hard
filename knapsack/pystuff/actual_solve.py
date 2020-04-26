import numpy as np

def admissible_exp(solution, n, items, K):
    wf = max(map(lambda x: x.value/x.weight, items))

    #current_weight = sum([ for x, item in zip()])

def solve(K, items):
    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0] * len(items)

    items_by_ratio = sorted(items, key=lambda x: x.value/x.weight, reverse=True)

    for item in items_by_ratio:
        if weight + item.weight <= K:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value, taken