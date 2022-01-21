import math
import random
import itertools
import sys
import statistics

# Question 3: Traveling Salesman Problem

def main():
    number_of_tsp = 100
    number_of_cities = 7

    tsp_instances = list()
    for i in range(number_of_tsp):
        tsp_instances.append(TSP(number_of_cities))

    # a) 
    print('Brute Force')
    costs = list()
    for i in range(len(tsp_instances)):
        tsp_instances[i].brute_force()
        costs.append(tsp_instances[i].current_cost)

    min_cost = min(costs)
    max_cost = max(costs)
    mean_cost = statistics.mean(costs)
    std_cost = statistics.stdev(costs)

    print("min: ", min_cost)
    print("max: ", max_cost)
    print("mean: ", mean_cost)
    print("std: ", std_cost)


    
    # b) Baseline

    # c) Hill Climbing

    # d) Scale up!

"""
Compute cost between two cities
a: tuple representing coordinates of city A
b: tuple representing coordinates of city B
"""
def cost(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

"""
Compute state cost
tour: array of tuples (cities)
"""
def state_cost(state):
    total_cost = 0
    for i in range(len(state)):
        total_cost += cost(state[i-1], state[i])
    return total_cost

"""
Compute state neighbours. The neighbours is the set of tours
resulting of all possible permutations of two cities in the
state.
"""
def state_neighbours(state):
    neighbours = list()

    # all possible combinations of indices
    combinations = list(itertools.combinations(range(len(state)), 2))

    for c in combinations:
        neighbour = state.copy()

        # permute cities
        tmp = neighbour[c[0]]
        neighbour[c[0]] = neighbour[c[1]]
        neighbour[c[1]] = tmp

        neighbours.append(neighbour)

    return neighbours

"""
TSP problem instance
"""
class TSP:
    def __init__(self, number_of_cities):
        self.current_state = list()
        self.neighbours = list()
        self.current_cost = 0
        for i in range(number_of_cities):
            self.current_state.append((random.random(), random.random()))
            self.neighbours = state_neighbours(self.current_state)
            self.current_cost = state_cost(self.current_state)
    
    """
    Solve by Brute Force
    Generate all possible city permutations and find the 
    tour with the minimum cost.
    """
    def brute_force(self):
        permutations = list(itertools.permutations(self.current_state, len(self.current_state)))
        min_cost = sys.float_info.max
        min_index = 0
        for i in range(len(permutations)):
            cost = state_cost(permutations[i])
            if cost < min_cost:
                min_cost = cost
                min_index = i
        self.current_state = permutations[min_index]
        self.current_cost = min_cost

if __name__ == "__main__":
    main()
