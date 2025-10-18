import numpy as np
from numpy import inf

# Given distance matrix for the problem
d = np.array([
    [0, 10, 12, 11, 14],
    [10, 0, 13, 15, 8],
    [12, 13, 0, 9, 14],
    [11, 15, 9, 0, 16],
    [14, 8, 14, 16, 0]
])

iteration = 100
n_ants = 5
n_citys = 5

# Initialization parameters
m = n_ants
n = n_citys
e = 0.5          # evaporation rate
alpha = 1        # pheromone factor
beta = 2         # visibility factor

# Calculating the visibility of the next city: visibility(i,j) = 1/d(i,j)
visibility = 1 / d
visibility[visibility == inf] = 0

# Initializing pheromone levels on all paths
pheromone = 0.1 * np.ones((n, n))

# Initializing the route of ants (n_ants x (n_citys + 1))
# Adding 1 because ants return to the starting city
route = np.ones((m, n + 1))

for ite in range(iteration):
    route[:, 0] = 1  # all ants start from city 1

    for i in range(m):
        temp_visibility = np.array(visibility)

        for j in range(n - 1):
            combine_feature = np.zeros(n)
            cum_prob = np.zeros(n)

            cur_loc = int(route[i, j] - 1)
            temp_visibility[:, cur_loc] = 0  # make current city's visibility 0

            p_feature = np.power(pheromone[cur_loc, :], alpha)
            v_feature = np.power(temp_visibility[cur_loc, :], beta)

            combine_feature = np.multiply(p_feature, v_feature)
            total = np.sum(combine_feature)

            if total == 0:
                probs = np.ones(n) / n
            else:
                probs = combine_feature / total

            cum_prob = np.cumsum(probs)
            r = np.random.random_sample()
            city = np.nonzero(cum_prob > r)[0][0] + 1
            route[i, j + 1] = city

        # Finding the last untraversed city and adding to route
        left = list(set([i for i in range(1, n + 1)]) - set(route[i, :-1]))[0]
        route[i, -1] = left

    # Calculate total distance for each ant
    route_opt = np.array(route)
    dist_cost = np.zeros((m, 1))

    for i in range(m):
        s = 0
        for j in range(n):
            s += d[int(route_opt[i, j]) - 1, int(route_opt[i, j + 1]) - 1]
        dist_cost[i] = s

    # Find best route and its cost
    dist_min_loc = np.argmin(dist_cost)
    dist_min_cost = dist_cost[dist_min_loc]
    best_route = route[dist_min_loc, :]

    # Pheromone evaporation
    pheromone = (1 - e) * pheromone

    # Update pheromone on all paths
    for i in range(m):
        for j in range(n):
            dt = 1 / dist_cost[i]
            pheromone[int(route_opt[i, j]) - 1, int(route_opt[i, j + 1]) - 1] += dt

print('Routes of all ants at the end:')
print(route_opt)
print()
print('Best path:', best_route)
print('Cost of the best path:', int(dist_min_cost[0]) + d[int(best_route[-1]) - 1, 0])
