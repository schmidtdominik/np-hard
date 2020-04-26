import itertools
import random
import time

import numpy as np

class Solver:

    def __init__(self, set_count, item_count, sets):
        self.set_count = set_count
        self.item_count = item_count

        self.costs = np.zeros(set_count)
        sets_unpacked = []
        self.worths = np.zeros(set_count)
        for i, s in enumerate(sets):
            items = set(s.items)
            sets_unpacked.append(items)
            self.costs[i] = s.cost
            self.worths[i] = len(items) / s.cost

        greedy_ordering = list(np.argsort(self.worths)[::-1])

        required_selection = np.zeros(set_count, dtype=np.bool)
        required_sets = []
        covered = set()
        for item in range(item_count):
            count = 0
            last_set_with_item = None
            for i, set_ in enumerate(sets_unpacked):
                if item in set_:
                    count += 1
                    last_set_with_item = i
            if count == 1:
                required_sets.append(last_set_with_item)
                required_selection[last_set_with_item] = True
                covered |= sets_unpacked[last_set_with_item]
                greedy_ordering.remove(last_set_with_item)

        # TODO: use this: self.sets_that_contain_item = []
        self.best_global_solution = None
        self.best_global_solution_cost = float('inf')

        #self.rare_items = [i for i in range(item_count) if sum(1 for s in sets_unpacked if i in s) < set_count/3] # TODO: tweak this
        #self.rare_item_sets = [set([i for i, s in enumerate(sets_unpacked) if j in s]) for j in self.rare_items]

        #print(self.rare_items)

        #self.prune_factor = 0.4
        #self.prune_factor_update = time.time()
        self.time_limit = 8
        self.start_time = time.time()
        self.enum(required_selection, np.array(greedy_ordering), covered, sum(self.costs[i] for i in required_sets), sets_unpacked, 0, set(required_sets), 99999999999)

        self.time_limit = 120
        self.start_time = time.time()
        for lds_limit in range(0, self.set_count):
            print('LDS:', lds_limit)
            self.enum(required_selection, np.array(greedy_ordering), covered, sum(self.costs[i] for i in required_sets), sets_unpacked, 0, set(required_sets), lds_limit)
            if time.time() - self.start_time > self.time_limit:
                break
        

    def enum(self, partial_solution, remaining_selection_ordered, covered, cost, sets_benefits, depth, selected_sets, lds_limit):
        """print(partial_solution)
        print(remaining_selection_ordered)
        print(covered)
        print(cost)
        print(self.costs)
        print(self.worths)
        print(self.sets_unpacked)"""

        """if time.time() - self.prune_factor_update > 0.3:
            self.prune_factor_update = time.time()
            self.prune_factor *= 1.01
            print('PF:', self.prune_factor)

        if random.random() < self.prune_factor and depth > 20:
            return"""

        if time.time() - self.start_time > self.time_limit:
            return

        # fully covered
        if len(covered) == self.item_count:
            if cost < self.best_global_solution_cost:
                print(cost)
                self.best_global_solution_cost = cost
                self.best_global_solution = partial_solution
            return

        # can't add more items but not yet done
        if len(remaining_selection_ordered) == 0:
            return

        # bound
        if cost >= self.best_global_solution_cost:
            return

        if self.set_count < 6000:
            local_worths = np.array([len(s) / self.costs[i] for i, s in enumerate(sets_benefits)])
            selecting_set_among_remaining = np.argmax(local_worths[remaining_selection_ordered])
            selecting_set = remaining_selection_ordered[selecting_set_among_remaining]
            #print(local_worths, selecting_set_among_remaining, selecting_set, remaining_selection_ordered)
            #print(len(remaining_selection_ordered))
            remaining_selection_ordered = remaining_selection_ordered[np.arange(len(remaining_selection_ordered)) != selecting_set_among_remaining].copy()
            #print(len(remaining_selection_ordered))

            #print(remaining_selection_ordered, depth, '\n')
        else:
            selecting_set = remaining_selection_ordered[0]
            remaining_selection_ordered = remaining_selection_ordered[1:]

        added_items = sets_benefits[selecting_set]
        if not added_items.issubset(covered):
            p1 = partial_solution.copy()
            p1[selecting_set] = True
            if self.set_count < 6000:
                pass_sets = [s-added_items for s in sets_benefits]
            else:
                pass_sets = sets_benefits
            self.enum(p1, remaining_selection_ordered, covered | added_items, cost + self.costs[selecting_set], pass_sets, depth + 1, selected_sets | {selecting_set}, lds_limit)

        # DONT USE THIS SET
        """total_possible_items = selected_sets | set(remaining_selection_ordered)
        for rare_set_family in self.rare_item_sets:
            if not (rare_set_family & total_possible_items):
                return"""

        if lds_limit > 0:
            p2 = partial_solution.copy()  # TODO: unnecessary?
            p2[selecting_set] = False  # TODO: unnecessary?
            self.enum(p2, remaining_selection_ordered, covered, cost, sets_benefits, depth+1, selected_sets, lds_limit-1)


def solve(set_count, item_count, sets):
    """solution = [0] * set_count
    coverted = set()

    for s in sets:
        solution[s.index] = 1
        coverted |= set(s.items)
        if len(coverted) >= item_count:
            break
    print(solution)
    return solution"""
    h = Solver(set_count, item_count, sets)
    #print(h.solution, h.cost)
    return list(h.best_global_solution.astype(np.int))
