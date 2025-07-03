#!/usr/bin/env python3
#Total distance: 46622.41
import random
import math
import sys
import time
from common import read_input, print_tour

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
# Best Insertion 法
# --------------------------
def best_insertion(cities):
    N = len(cities)
    unvisited = set(range(N))
    tour = [0]
    unvisited.remove(0)

    # 最も近い都市を追加
    nearest = min(unvisited, key=lambda x: distance(cities[0], cities[x]))
    tour.append(nearest)
    unvisited.remove(nearest)

    step = 0
    while unvisited:
        step += 1
        if step % 50 == 0 or not unvisited:
            progress = 100 * (N - len(unvisited)) / N
            print(f"[Best Insertion] Progress: {progress:.2f}%", end="\r")

        best_city, best_pos = None, None
        min_increase = float('inf')
        for city in unvisited:
            for i in range(len(tour)):
                a = cities[tour[i - 1]]
                b = cities[tour[i]]
                c = cities[city]
                increase = distance(a, c) + distance(c, b) - distance(a, b)
                if increase < min_increase:
                    best_city, best_pos = city, i
                    min_increase = increase

        tour.insert(best_pos, best_city)
        unvisited.remove(best_city)

    print("\n[Best Insertion] Completed. Tour length:", len(tour))
    return tour

# --------------------------
# 焼きなまし法 (Simulated Annealing)
# --------------------------
def simulated_annealing(tour, cities, initial_temp=800.0, cooling_rate=0.999, time_limit=10.0):
    start_time = time.time()

    current = tour[:]
    best = tour[:]
    current_cost = best_cost = total_distance(current, cities)
    T = initial_temp
    iteration = 0

    while time.time() - start_time < time_limit:
        iteration += 1
        i, j = sorted(random.sample(range(len(tour)), 2))
        neighbor = current[:i] + list(reversed(current[i:j])) + current[j:]
        neighbor_cost = total_distance(neighbor, cities)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best = current
                best_cost = current_cost

        T *= cooling_rate

        if iteration % 100 == 0:
            elapsed = time.time() - start_time
            print(f"[SA] Iteration {iteration}, Temp={T:.2f}, Cost={current_cost:.2f}, Elapsed={elapsed:.2f} sec", end='\r')

    print(f"\n[SA] Finished in {time.time() - start_time:.2f} sec, Best Cost: {best_cost:.2f}")
    return best

# --------------------------
# 高速 2-opt 法
# --------------------------
def two_opt_fast(tour, cities, time_limit=10.0):
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

# --------------------------
# メインソルバー
# --------------------------
def solve(cities):
    initial_tour = best_insertion(cities)
    best_tour = None
    best_distance = float('inf')

    for i in range(5):  # 複数試行
        print(f"\n[Run {i+1}/5] Starting SA...")
        sa_tour = simulated_annealing(initial_tour, cities,
                                      initial_temp=500.0,
                                      cooling_rate=0.999,
                                      time_limit=5.0)
        sa_tour = two_opt_fast(sa_tour, cities, time_limit=2.0)
        dist = total_distance(sa_tour, cities)
        print(f"[Run {i+1}] Total distance: {dist:.2f}")
        if dist < best_distance:
            best_tour = sa_tour
            best_distance = dist

    # 最後に深めの2-optで微調整
    best_tour = two_opt_fast(best_tour, cities, time_limit=5.0)
    print(f"\n[Final] Best total distance: {best_distance:.2f}")
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