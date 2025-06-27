import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])


def total_distance(tour, cities):
    return sum(
        distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )


def greedy_tour(cities):
    N = len(cities)
    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited = set(range(1, N))
    tour = [current_city]

    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        unvisited.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    return tour


def two_opt(tour, cities):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:  # 隣接はスキップ
                    continue
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                if total_distance(new_tour, cities) < total_distance(tour, cities):
                    tour = new_tour
                    improved = True
        # 1回の改善でbreakしないと遅くなるので、1改善ごとに再スタート
    return tour


def solve(cities):
    initial_tour = greedy_tour(cities)
    improved_tour = two_opt(initial_tour, cities)
    return improved_tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    total = total_distance(tour, read_input(sys.argv[1]))
    print(f"Total distance: {total:.2f}")