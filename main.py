import math
import random
import multiprocessing
import matplotlib.pyplot as plt


def distance(c1, c2):
    return math.hypot(c1[0] - c2[0], c1[1] - c2[1])


def route_distance(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))


def two_opt(route, dist_matrix):
    """Local search polish to uncross paths for an individual ant."""
    best_route = list(route)
    best_dist = route_distance(best_route, dist_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(len(route) - 1):
            for j in range(i + 2, len(route) + (i > 0)):
                new_route = best_route[:i + 1] + best_route[i + 1:j + 1][::-1] + best_route[j + 1:]
                new_dist = route_distance(new_route, dist_matrix)
                if new_dist < best_dist:
                    best_route = new_route
                    best_dist = new_dist
                    improved = True
    return best_route


def run_single_ant(args):
    """Generates a route for a single ant using current pheromones."""
    start_city, pheromones, alpha, beta, n, dist_matrix = args
    route = [start_city]
    unvisited = set(range(n))
    unvisited.remove(start_city)

    while unvisited:
        current = route[-1]
        probabilities = []
        total = 0.0

        for next_city in unvisited:
            d = dist_matrix[current][next_city]
            tau = pheromones[current][next_city] ** alpha
            eta = (1.0 / max(d, 0.0001)) ** beta
            val = tau * eta
            probabilities.append((next_city, val))
            total += val

        r = random.uniform(0, total)
        cumulative = 0.0
        chosen = list(unvisited)[0]  # fallback
        for city_id, val in probabilities:
            cumulative += val
            if cumulative >= r:
                chosen = city_id
                break
        unvisited.remove(chosen)
        route.append(chosen)

    # Polish with 2-opt
    polished_route = two_opt(route, dist_matrix)
    dist = route_distance(polished_route, dist_matrix)
    return polished_route, dist


def parallel_ant_colony(cities, dist_matrix, num_ants=24, iterations=30, alpha=1.0, beta=3.0, evaporation=0.5, q=100):
    n = len(cities)
    pheromones = [[1.0 for _ in range(n)] for _ in range(n)]

    best_overall_route = None
    best_overall_dist = float('inf')

    num_cores = multiprocessing.cpu_count()
    print(f"\nLaunching ACO across {num_cores} available CPU cores for {n} cities...")

    with multiprocessing.Pool(processes=num_cores) as pool:
        for iteration in range(iterations):
            ant_args = [
                (random.randint(0, n - 1), pheromones, alpha, beta, n, dist_matrix)
                for _ in range(num_ants)
            ]

            results = pool.map(run_single_ant, ant_args)

            all_ant_routes = []
            for polished_route, dist in results:
                if dist < best_overall_dist:
                    best_overall_dist = dist
                    best_overall_route = polished_route
                all_ant_routes.append((polished_route, dist))

            for i in range(n):
                for j in range(n):
                    pheromones[i][j] *= (1.0 - evaporation)

            for route, dist in all_ant_routes:
                deposit = q / dist
                for i in range(n):
                    c1 = route[i]
                    c2 = route[(i + 1) % n]
                    pheromones[c1][c2] += deposit
                    pheromones[c2][c1] += deposit

            print(f"Iteration {iteration + 1:2d}/{iterations} | Best Distance: {best_overall_dist:.2f}")

    return best_overall_route, best_overall_dist


def plot_route(cities, route, distance_val):
    x = [c[0] for c in cities]
    y = [c[1] for c in cities]

    route_x = [cities[i][0] for i in route] + [cities[route[0]][0]]
    route_y = [cities[i][1] for i in route] + [cities[route[0]][1]]

    plt.figure(figsize=(10, 8))
    plt.plot(route_x, route_y, color='royalblue', linestyle='-', linewidth=1.5, zorder=1, label='Optimized Route')
    plt.scatter(x, y, color='crimson', s=40, zorder=2, label='Cities')
    plt.scatter(cities[route[0]][0], cities[route[0]][1], color='gold', s=120, marker='*', zorder=3,
                label='Start/End City')

    plt.title(f"Traveling Salesman Problem ({len(cities)} Cities) - Total Distance: {distance_val:.2f}", fontsize=14,
              fontweight='bold')
    plt.xlabel("X Coordinate", fontsize=11)
    plt.ylabel("Y Coordinate", fontsize=11)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    random.seed(42)
    print("--- Parallel ACO TSP Solver ---")

    # Ask user for input with safety fallbacks
    try:
        num_cities = int(input("Enter the number of cities to travel to: "))
        if num_cities < 3:
            print("Warning: A minimum of 3 cities is required. Defaulting to 10.")
            num_cities = 10
    except ValueError:
        print("Invalid input received. Defaulting to 50 cities.")
        num_cities = 50

    # Generate consistent map data based on user choice
    cities = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(num_cities)]
    dist_matrix = [[distance(c1, c2) for c2 in cities] for c1 in cities]

    # Run optimization
    final_route, final_dist = parallel_ant_colony(cities, dist_matrix)
    print(f"\nOptimization Finished! Final Distance: {final_dist:.2f}")

    # Render plot
    plot_route(cities, final_route, final_dist)