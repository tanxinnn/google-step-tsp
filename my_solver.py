#!/usr/bin/env python3

from common import format_tour, read_input

import my_greedy
import solver_greedy    
import solver_random    
import my_insertion

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        for solver, name in ((my_greedy, 'greedy'), (my_insertion, 'insertion'),):
            tour = solver.solve(cities)
            with open(f'sample/{name}_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    generate_sample_output()
