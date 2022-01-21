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

    # a) Solve each TSP by brute-force
    print('Solution')
    costs = list()
    for i in range(len(tsp_instances)):
        tsp_instances[i].optimal_state, tsp_instances[i].optimal_cost = tsp_instances[i].brute_force()
        costs.append(tsp_instances[i].optimal_cost)

    min_cost = min(costs)
    max_cost = max(costs)
    mean_cost = statistics.mean(costs)
    std_cost = statistics.stdev(costs)

    print("min: {min_cost:.6f}".format(min_cost=min_cost))
    print("max: {max_cost:.6f}".format(max_cost=max_cost))
    print("mean: {mean_cost:.6f}".format(mean_cost=mean_cost))
    print("std: {std_cost:.6f}\n".format(std_cost=std_cost))


    # b) Baseline
    print('Baseline')
    costs = list()
    for i in range(len(tsp_instances)):
        costs.append(state_cost(tsp_instances[i].initial_state))

    min_cost = min(costs)
    max_cost = max(costs)
    mean_cost = statistics.mean(costs)
    std_cost = statistics.stdev(costs)

    print("min: {min_cost:.6f}".format(min_cost=min_cost))
    print("max: {max_cost:.6f}".format(max_cost=max_cost))
    print("mean: {mean_cost:.6f}".format(mean_cost=mean_cost))
    print("std: {std_cost:.6f}\n".format(std_cost=std_cost))


    # c) Hill Climbing
    print('Hill Climbing')
    costs = list()
    optimal_count = 0
    for i in range(len(tsp_instances)):
        final_state, final_cost = tsp_instances[i].hill_climbing()
        if final_cost <= tsp_instances[i].optimal_cost:
            optimal_count += 1
        costs.append(final_cost)
        

    min_cost = min(costs)
    max_cost = max(costs)
    mean_cost = statistics.mean(costs)
    std_cost = statistics.stdev(costs)

    print("min: {min_cost:.6f}".format(min_cost=min_cost))
    print("max: {max_cost:.6f}".format(max_cost=max_cost))
    print("mean: {mean_cost:.6f}".format(mean_cost=mean_cost))
    print("std: {std_cost:.6f}".format(std_cost=std_cost))
    print("{optimal_count} instances found the optimal solution.\n".format(optimal_count=optimal_count))
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
        # initial config
        self.initial_state = list()

        # optimal config
        self.optimal_state = list()
        self.optimal_cost = sys.float_info.max

        # generate random city coordinates
        for i in range(number_of_cities):
            self.initial_state.append((random.random(), random.random()))
    
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
        return (permutations[min_index], min_cost)

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
                return (current_state, current_cost)
            else:
                # take a greedy step towards local optimum
                current_state = neighbours[min_index]
                current_cost = min_cost


if __name__ == "__main__":
    main()
