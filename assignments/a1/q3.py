import math
import random
import itertools
import sys
import statistics

# Question 3: Traveling Salesman Problem

def main():
    number_of_tsp = 100
    number_of_cities = 7
    print('number of cities: {number_of_cities}'.format(number_of_cities=number_of_cities))
    print('number of TSP instances: {number_of_tsp}\n'.format(number_of_tsp=number_of_tsp))

    tsp_instances = list()
    for i in range(number_of_tsp):
        tsp_instances.append(TSP(number_of_cities))

    # a) Brute-Force
    # Solve each TSP by brute-force
    print('Brute-Force Solution')
    costs = list()
    for i in range(len(tsp_instances)):
        tsp_instances[i].optimal_cost = tsp_instances[i].brute_force()
        costs.append(tsp_instances[i].optimal_cost)
    print_stats(costs)

    # b) Baseline
    # Compute the costs of the initial state of each TSP instance.
    # Keep track of how many initial states are optimal
    print('Baseline')
    optimal_count = 0 
    costs = list()
    for i in range(len(tsp_instances)):
        cost = state_cost(tsp_instances[i].initial_state)
        costs.append(cost)
        if cost == tsp_instances[i].optimal_cost:
            optimal_count += 1

    print_stats(costs)
    print("{optimal_count}/{number_of_tsp} tsp instances were initialized as an optimal solution.\n".format(optimal_count=optimal_count, number_of_tsp=number_of_tsp))

    # c) Hill Climbing
    # Solve each TSP using Hill climbing. Keep track of how many instances will end 
    # up finding the optimal solution
    print('Hill Climbing')
    costs = list()
    optimal_count = 0
    for i in range(len(tsp_instances)):
        final_cost = tsp_instances[i].hill_climbing()
        if final_cost <= tsp_instances[i].optimal_cost:
            optimal_count += 1
        costs.append(final_cost)

    print_stats(costs)
    print("{optimal_count}/{number_of_tsp} tsp instances found an optimal solution using hill climbing.\n".format(optimal_count=optimal_count, number_of_tsp=number_of_tsp))
    
    # d) Scale up to 100 cities and repeat part b) and c)
    print("Scaling up!\n")
    number_of_cities = 100
    tsp_instances = list()

    for i in range(number_of_tsp):
        tsp_instances.append(TSP(number_of_cities))

    print('number of cities: {number_of_cities}'.format(number_of_cities=number_of_cities))
    print('number of TSP instances: {number_of_tsp}\n'.format(number_of_tsp=number_of_tsp))

    print('Baseline')
    costs = list()
    for i in range(len(tsp_instances)):
        costs.append(state_cost(tsp_instances[i].initial_state))
    print_stats(costs)

    print('Hill Climbing')
    costs = list()
    optimal_count = 0
    for i in range(len(tsp_instances)):
        final_cost = tsp_instances[i].hill_climbing()
        costs.append(final_cost)
    print_stats(costs)


# ---------------- HELPER FUNCTIONS ---------------- #
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

'''
Print statistics of sample list: min, max, mean , std
'''
def print_stats(sample):
    print("min: {min:.6f}".format(min=min(sample)))
    print("max: {max:.6f}".format(max=max(sample)))
    print("mean: {mean:.6f}".format(mean=statistics.mean(sample)))
    print("std: {std:.6f}\n".format(std=statistics.stdev(sample)))

# ---------------- HELPER CLASSES ---------------- #
"""
TSP problem instance
"""
class TSP:
    def __init__(self, number_of_cities):
        # initial config
        self.initial_state = list()

        # generate random city coordinates
        for i in range(number_of_cities):
            while(True):
                element = (random.random(), random.random())
                if element not in self.initial_state:
                    self.initial_state.append(element)
                    break
    
    """
    Solve by Brute Force
    returns the following tuple (optimal_state, optimal_cost)
    """
    def brute_force(self):
        permutations = list(itertools.permutations(self.initial_state, len(self.initial_state)))
        min_cost = sys.float_info.max
        min_index = 0
        for i in range(len(permutations)):
            cost = state_cost(permutations[i])
            if cost < min_cost:
                min_cost = cost
                min_index = i
        return min_cost

    """
    Solve by Hill Climbing
    returns the following tuple (final_state, final_cost)
    """
    def hill_climbing(self):
        # initialization
        current_state = self.initial_state
        current_cost = state_cost(self.initial_state)

        # repeat until local minimum found
        while(True):
            min_cost = sys.float_info.max
            min_index = 0
            # generate set of neighbours of current state
            neighbours = state_neighbours(current_state)

            for i in range(len(neighbours)):
                cost = state_cost(neighbours[i])
                if cost < min_cost:
                    min_cost = cost
                    min_index = i

            if min_cost >= current_cost:
                # we are at a local min
                return current_cost
            else:
                # take a greedy step towards local optimum
                current_state = neighbours[min_index]
                current_cost = min_cost


if __name__ == "__main__":
    main()
