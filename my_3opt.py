#!/usr/bin/env python3
#Total distance: 46532.49 (best_insertion,time-limit=5.0)
#Total distance: 46461.10(greedy_insertion,time-limit=5.0)
#Total distance: 46065.63(time-limit=20.0)
#2opt, 3opt iteration 152: 43853.30
#2opt, 3opt ieration 152: 88705.54
import random
import math
import sys
import time
from common import read_input, print_tour
import pickle

# --------------------------
# 距離関数・合計距離関数
# --------------------------
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def total_distance(tour, cities):
    return sum(
        distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )

# --------------------------
# 貪欲法
# --------------------------
def greedy_insertion(cities):
    N = len(cities)
    unvisited = set(range(N))

    # 全体で一番近い2都市を探して開始
    best_pair = None
    min_dist = float('inf')
    for i in range(N):
        for j in range(i + 1, N):
            d = distance(cities[i], cities[j])
            if d < min_dist:
                min_dist = d
                best_pair = (i, j)

    tour = [best_pair[0], best_pair[1]]
    unvisited.remove(best_pair[0])
    unvisited.remove(best_pair[1])

    while unvisited:
        percentage = (len(unvisited) / N) * 100
        print(f"[Greedy Insertion] Remaining: {len(unvisited)} cities ({percentage:.2f}%)", end='\r')
        best_city, best_pos, min_increase = None, None, float('inf')
        for city in unvisited:
            for i in range(len(tour)):
                a = cities[tour[i - 1]]
                b = cities[tour[i]]
                c = cities[city]
                increase = distance(a, c) + distance(c, b) - distance(a, b)
                if increase < min_increase:
                    best_city, best_pos, min_increase = city, i, increase

        tour.insert(best_pos, best_city)
        unvisited.remove(best_city)
    return tour

# --------------------------
# 2-opt 法
# --------------------------
def two_opt_fast(tour, cities):
    N = len(tour)
    loop_count = 0
    start_time = time.time()

    while True:
        loop_count += 1
        improved = False

        if loop_count % 10 == 0:
            elapsed = time.time() - start_time
            print(f"[2-opt] Iteration {loop_count}, Elapsed: {elapsed:.2f} sec, Distance: {total_distance(tour, cities):.2f}")

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
        if not improved:
            break

    print(f"[2-opt] Completed in {loop_count} iterations, Final distance: {total_distance(tour, cities):.2f}")
    return tour


# --------------------------
# 3-opt 法
# --------------------------
def three_opt(tour, cities):
    N = len(tour)
    improved = True
    count = 0
    start_time = time.time()

    def dist(a, b):
        return distance(cities[a], cities[b])

    try:
        while improved and count < 152:
            improved = False
            count += 1

            if count % 2 == 0:
                elapsed = time.time() - start_time
                print(f"[3-opt] Iteration {count}, Elapsed: {elapsed:.2f} sec, Distance: {total_distance(tour, cities):.2f}")

            for i in range(N - 5):
                for j in range(i + 2, N - 2):
                    for k in range(j + 2, N if i > 0 else N - 1):
                        A, B = tour[i], tour[i + 1]
                        C, D = tour[j], tour[j + 1]
                        E, F = tour[k], tour[(k + 1) % N]

<<<<<<< HEAD
                    # 3-opt 交換パターンのうち代表的なものを試す
                    # パターン 1: reverse B-C
                    d1 = dist(A, C) + dist(B, D) + dist(E, F)
                    if d1 < d0:
                        tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                        improved = True
                        d0=d1
                        break

                    # パターン 2: reverse D-E
                    d2 = dist(A, B) + dist(C, E) + dist(D, F)
                    if d2 < d0:
                        tour[j + 1:k + 1] = reversed(tour[j + 1:k + 1])
                        improved = True
                        d0=d2
                        break

                    # パターン 3: reverse B-C and D-E
                    d3 = dist(A, C) + dist(B, E) + dist(D, F)
                    if d3 < d0:
                        tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                        tour[j + 1:k + 1] = reversed(tour[j + 1:k + 1])
                        improved = True
                        break

=======
                        d0 = dist(A, B) + dist(C, D) + dist(E, F)

                        d1 = dist(A, C) + dist(B, D) + dist(E, F)
                        if d1 < d0:
                            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                            improved = True
                            break

                        d2 = dist(A, B) + dist(C, E) + dist(D, F)
                        if d2 < d0:
                            tour[j + 1:k + 1] = reversed(tour[j + 1:k + 1])
                            improved = True
                            break

                        d3 = dist(A, C) + dist(B, E) + dist(D, F)
                        if d3 < d0:
                            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                            tour[j + 1:k + 1] = reversed(tour[j + 1:k + 1])
                            improved = True
                            break

                    if improved:
                        break
>>>>>>> 5e3e18d (Update)
                if improved:
                    break

        print(f"[3-opt] Finished after {count} iterations, Final distance: {total_distance(tour, cities):.2f}")
        return tour
    except KeyboardInterrupt:
        with open("output_file", "wb") as f:
            pickle.dump(tour, f)
        print('[3-opt] Interrupted, tour saved to output_file')


# --------------------------
# メインソルバー
# --------------------------
def solve(cities):
    #initial_tour = greedy_insertion(cities)
    tour=list(range(len(cities)))
    best_tour = two_opt_fast(tour, cities)
    # 最後に3-optで調整
    best_tour = three_opt(best_tour, cities)
    return best_tour

# --------------------------
# メイン処理
# --------------------------
if __name__ == '__main__':
    assert len(sys.argv) > 1
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    cities = read_input(input_file)
    tour = solve(cities)
    print_tour(tour)

    if output_file:
        with open(output_file, "w") as f:
            f.write("index\n")
            for city in tour:
                f.write(f"{city}\n")

    print(f"Total distance: {total_distance(tour, cities):.2f}")
