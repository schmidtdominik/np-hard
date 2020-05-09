import heapq
import math
import random

from colorit import color_back


class Pool:
    def __init__(self, k=8):
        self.k = k
        self.heap = []
        self.best = float('inf')
        self.t = 1000
        self.acc = 0
        self.nacc = 0

    def get_random(self):
        return random.choice(self.heap)[1].copy()

    def push(self, solution, value):

        self.t = max(1, self.t-0.01)
        if len(self.heap) < self.k:
            if value < self.best:
                #print(color_back('UPGRADE_I: ' + str(value), 190, 250, 190))
                print(color_back('*', 190, 250, 190), end='')
            self.best = min(self.best, value)
            heapq.heappush(self.heap, (-value, solution))
        elif value < -self.heap[0][0]:
            if value < self.best:
                #print(color_back('UPGRADE: ' + str(value), 190, 250, 190))
                print(color_back('*', 190, 250, 190), end='')
            self.best = min(self.best, value)
            heapq.heapreplace(self.heap, (-value, solution))
        elif random.random() < math.exp(-abs(value - self.heap[0][0]) / self.t):
            if value < self.best:
                #print(color_back('UPGRADE: ' + str(value), 190, 250, 190))
                print(color_back('*', 190, 250, 190), end='')
            self.best = min(self.best, value)
            heapq.heapreplace(self.heap, (-value, solution))
            self.acc += 1
        else:
            self.nacc +=1


    def print_acc_stats(self):
        print(self.acc/(self.acc+self.nacc+0.01), self.acc, self.nacc)


    def get_best(self): # slow!
        v = min(self.heap, key=lambda x: -x[0])
        return -v[0], v[1]

    def sorted(self):
        return [y[1] for y in sorted(self.heap, key=lambda x: -x[0])]

    def rebase(self):
        self.heap =[min(self.heap, key=lambda x: -x[0])]
        self.best = -self.heap[0][0]

    def print_stats(self):
        print(f'[POOL] worst={-self.heap[0][0]} best={self.get_best()[0]} all={[-v[0] for v in self.heap]}')

    def clear(self):
        self.heap = []
        self.best = float('inf')
