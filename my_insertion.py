#!/usr/bin/env python3

import sys
import math
import time
from common import read_input, print_tour


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def total_distance(tour, cities):
    return sum(
        distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )


def best_insertion(cities):
    N = len(cities)
    unvisited = set(range(N))
    tour = [0]
    unvisited.remove(0)

    # 最も近い都市を1つ追加
    nearest = min(unvisited, key=lambda x: distance(cities[0], cities[x]))
    tour.append(nearest)
    unvisited.remove(nearest)

    while unvisited:
        progress=100*(N-len(unvisited))/N
        print(f"[Best Insertion] Progress: {progress:.2f}%")
        best_city = None
        best_pos = None
        min_increase = float('inf')

        for city in unvisited:
            for i in range(len(tour)):
                a = cities[tour[i - 1]]
                b = cities[tour[i]]
                c = cities[city]
                increase = distance(a, c) + distance(c, b) - distance(a, b)
                if increase < min_increase:
                    best_city = city
                    best_pos = i
                    min_increase = increase

        tour.insert(best_pos, best_city)
        unvisited.remove(best_city)
    print("[Best Insertion] Completed. Tour length:", len(tour))
    return tour


def two_opt_fast(tour, cities, time_limit=3.0):
    start_time = time.time()
    N = len(tour)
    loop_count = 0

    while time.time() - start_time < time_limit:
        loop_count += 1
        improved = False
        print(f"[2-opt] Iteration {loop_count}, elapsed: {time.time() - start_time:.2f} sec", end="\r")

        for i in range(1, N - 2):
            for j in range(i + 2, N):
                if j - i == 1:
                    continue
                a, b = tour[i - 1], tour[i]
                c, d = tour[j - 1], tour[j % N]
                before = distance(cities[a], cities[b]) + distance(cities[c], cities[d])
                after = distance(cities[a], cities[c]) + distance(cities[b], cities[d])
                if after < before:
                    tour[i:j] = reversed(tour[i:j])
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break

    print(f"\n[2-opt] Completed {loop_count} iterations in {time.time() - start_time:.2f} seconds.")
    return tour


def solve(cities):
    tour = best_insertion(cities)             # 初期解：Best Insertion
    tour = two_opt_fast(tour, cities, 3.0)    # 高速版 2-opt（3秒制限）
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    cities = read_input(input_file)
    tour = solve(cities)
    print_tour(tour)
    
    with open(output_file, "w") as f:
        f.write("index\n")
        for city in tour:
            f.write(f"{city}\n")
    print(f"Total distance: {total_distance(tour, cities):.2f}")
