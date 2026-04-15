import random

# Number of cities
N = 8

# Adjacency Matrix
dist = [
    [0, 10, 15, 20, 25, 30, 35, 40],
    [12, 0, 35, 15, 20, 25, 30, 45],
    [25, 30, 0, 10, 40, 20, 15, 35],
    [18, 25, 12, 0, 15, 30, 20, 10],
    [22, 18, 28, 20, 0, 15, 25, 30],
    [35, 22, 18, 28, 12, 0, 40, 20],
    [30, 35, 22, 18, 28, 32, 0, 15],
    [40, 28, 35, 22, 18, 25, 12, 0]
]

# Calculate tour cost
def tour_cost(path):
    total = 0
    for i in range(N - 1):
        total += dist[path[i]][path[i + 1]]
    total += dist[path[N - 1]][path[0]]
    return total

# Generate neighbors by swapping
def generate_neighbors(path):
    neighbors = []
    for i in range(1, N):
        for j in range(i + 1, N):
            new_path = path[:]
            new_path[i], new_path[j] = new_path[j], new_path[i]
            neighbors.append(new_path)
    return neighbors

# Local Beam Search with state tracking
def local_beam_search(k, max_iter=100):
    states = []

    # Random initial states
    for _ in range(k):
        path = list(range(N))
        random.shuffle(path)
        states.append(path)

    best_path = None
    best_cost = float('inf')
    state_history = []
    iteration_count = 0

    for iteration in range(max_iter):
        all_neighbors = []

        for state in states:
            neighbors = generate_neighbors(state)
            all_neighbors.extend(neighbors)

        all_neighbors.sort(key=lambda x: tour_cost(x))
        states = all_neighbors[:k]

        # Record state costs for this iteration
        iteration_costs = [tour_cost(state) for state in states]
        state_history.append({
            'iteration': iteration + 1,
            'states': states[:],
            'costs': iteration_costs,
            'best_cost': iteration_costs[0],
            'worst_cost': iteration_costs[-1],
            'avg_cost': sum(iteration_costs) / len(iteration_costs)
        })

        current_best_cost = tour_cost(states[0])

        if current_best_cost < best_cost:
            best_cost = current_best_cost
            best_path = states[0]
            iteration_count = iteration + 1
        else:
            break

    return best_path, best_cost, state_history, iteration_count


print("LOCAL BEAM SEARCH RESULTS\n")

# Collect results for comparative table
results = []
for k in [3, 5, 10]:
    path, cost, state_history, iterations = local_beam_search(k)
    results.append({
        'Beam Width (k)': k,
        'Best Path': str(path),
        'Tour Cost': cost,
        'Iterations': iterations,
        'State History': state_history
    })

# Display comparative results table
print("{:<15} {:<45} {:<15} {:<15}".format("Beam Width (k)", "Best Path", "Tour Cost", "Iterations"))
print("-" * 90)
for result in results:
    print("{:<15} {:<45} {:<15} {:<15}".format(
        result['Beam Width (k)'],
        result['Best Path'],
        result['Tour Cost'],
        result['Iterations']
    ))
print("\n" + "="*90)
print("STATE COMPARISON - Iteration Metrics for Each Beam Width\n")

for result in results:
    k = result['Beam Width (k)']
    print(f"\nBeam Width k = {k}")
    print("{:<12} {:<15} {:<15} {:<15} {:<15}".format(
        "Iteration", "Best Cost", "Worst Cost", "Avg Cost", "Cost Range"
    ))
    print("-" * 72)
    
    for record in result['State History']:
        cost_range = record['worst_cost'] - record['best_cost']
        print("{:<12} {:<15} {:<15} {:<15.2f} {:<15}".format(
            record['iteration'],
            record['best_cost'],
            record['worst_cost'],
            record['avg_cost'],
            cost_range
        ))
print("\n" + "="*90)
print("DETAILED ITERATION ANALYSIS - ALL ITERATIONS\n")

for result in results:
    k = result['Beam Width (k)']
    print(f"\n{'='*90}")
    print(f"BEAM WIDTH k = {k}")
    print(f"{'='*90}")
    print("{:<12} {:<15} {:<15} {:<15} {:<15}".format(
        "Iteration", "Best Cost", "Worst Cost", "Avg Cost", "Cost Range"
    ))
    print("-" * 72)
    
    for record in result['State History']:
        cost_range = record['worst_cost'] - record['best_cost']
        print("{:<12} {:<15} {:<15} {:<15.2f} {:<15}".format(
            record['iteration'],
            record['best_cost'],
            record['worst_cost'],
            record['avg_cost'],
            cost_range
        ))
    
    # Show all states for each iteration
    print(f"\n--- Detailed States for k = {k} ---")
    for record in result['State History']:
        print(f"\nIteration {record['iteration']}:")
        for i, (state, cost) in enumerate(zip(record['states'], record['costs']), 1):
            print(f"  State {i}: {state} | Cost: {cost}")
print()