#!/usr/bin/env python3

from common import format_tour, read_input

from my_greedy import solve, total_distance
import solver_random

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        tour = solve(cities)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')
        total = total_distance(tour, cities)
        print(f'Challenge {i} : Total distance = {total}')

            


if __name__ == '__main__':
    generate_sample_output()