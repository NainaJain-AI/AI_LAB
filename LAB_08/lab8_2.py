import random

N = 8

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

# Tour cost
def tour_cost(path):
    total = 0
    for i in range(N - 1):
        total += dist[path[i]][path[i + 1]]
    total += dist[path[N - 1]][path[0]]
    return total

# Fitness
def fitness(path):
    return 1 / tour_cost(path)

# Selection (Tournament)
def selection(population):
    a = random.choice(population)
    b = random.choice(population)
    if fitness(a) > fitness(b):
        return a
    return b

# One Point Crossover
def one_point_crossover(p1, p2):
    point = random.randint(1, N - 2)
    child = p1[:point]

    for city in p2:
        if city not in child:
            child.append(city)

    return child

# Two Point Crossover
def two_point_crossover(p1, p2):
    point1 = random.randint(1, N - 3)
    point2 = random.randint(point1 + 1, N - 2)

    child = [-1] * N

    for i in range(point1, point2):
        child[i] = p1[i]

    index = 0
    for city in p2:
        if city not in child:
            while child[index] != -1:
                index += 1
            child[index] = city

    return child

# Mutation
def mutate(path, mutation_rate=0.1):
    was_mutated = False
    if random.random() < mutation_rate:
        i = random.randint(1, N - 1)
        j = random.randint(1, N - 1)
        path[i], path[j] = path[j], path[i]
        was_mutated = True
    return path, was_mutated

# Genetic Algorithm
def genetic_algorithm(crossover_type="one", pop_size=20, generations=200, track_stats=False):
    population = []

    for _ in range(pop_size):
        path = list(range(N))
        random.shuffle(path)
        population.append(path)

    best_path = None
    best_cost = float('inf')
    children_list = []
    generation_stats = []

    for gen in range(generations):
        new_population = []
        children_costs = []
        mutated_children = 0
        non_mutated_children = 0

        for i in range(pop_size):
            parent1 = selection(population)
            parent2 = selection(population)

            if crossover_type == "one":
                child = one_point_crossover(parent1, parent2)
            else:
                child = two_point_crossover(parent1, parent2)

            child, was_mutated = mutate(child)
            if was_mutated:
                mutated_children += 1
            else:
                non_mutated_children += 1
                
            child_cost = tour_cost(child)
            new_population.append(child)
            children_costs.append(child_cost)
            
            # Track children for display (limit to first 3 generations for clarity)
            if gen < 3:
                children_list.append({
                    'Generation': gen + 1,
                    'Child Index': i + 1,
                    'Path': child,
                    'Cost': child_cost,
                    'Mutated': 'Yes' if was_mutated else 'No'
                })

        # Calculate generation statistics
        min_cost = min(children_costs)
        max_cost = max(children_costs)
        avg_cost = sum(children_costs) / len(children_costs)
        
        generation_stats.append({
            'Generation': gen + 1,
            'Best Child Cost': min_cost,
            'Worst Child Cost': max_cost,
            'Avg Child Cost': avg_cost,
            'Total Children': len(children_costs),
            'Mutated': mutated_children,
            'Not Mutated': non_mutated_children
        })

        population = new_population

        for p in population:
            c = tour_cost(p)
            if c < best_cost:
                best_cost = c
                best_path = p

    return best_path, best_cost, children_list, generation_stats


print("GENETIC ALGORITHM RESULTS\n")

# Collect results for comparative table
results = []

# One Point
path1, cost1, children1, gen_stats1 = genetic_algorithm("one")
results.append({
    'Crossover Type': 'One Point',
    'Best Path': str(path1),
    'Tour Cost': cost1,
    'Children List': children1,
    'Generation Stats': gen_stats1
})

# Two Point
path2, cost2, children2, gen_stats2 = genetic_algorithm("two")
results.append({
    'Crossover Type': 'Two Point',
    'Best Path': str(path2),
    'Tour Cost': cost2,
    'Children List': children2,
    'Generation Stats': gen_stats2
})

# Display comparative results table
print("{:<18} {:<45} {:<12}".format(
    "Crossover Type", "Best Path", "Tour Cost"))
print("-" * 75)
for result in results:
    print("{:<18} {:<45} {:<12}".format(
        result['Crossover Type'],
        result['Best Path'],
        result['Tour Cost']
    ))
print()

# Display children generated (first 3 generations)
print("\n" + "="*100)
print("CHILDREN GENERATED - Detailed List (First 3 Generations)\n")

for result in results:
    print(f"\n{result['Crossover Type']} Crossover - Children Details:")
    print("{:<12} {:<12} {:<45} {:<12} {:<12}".format(
        "Generation", "Child ID", "Path", "Cost", "Mutated"))
    print("-" * 93)
    
    for child in result['Children List']:
        print("{:<12} {:<12} {:<45} {:<12} {:<12}".format(
            child['Generation'],
            child['Child Index'],
            str(child['Path']),
            child['Cost'],
            child['Mutated']
        ))
    print()

# Display generation statistics
print("\n" + "="*100)
print("GENERATION STATISTICS - Cost Metrics & Mutation Tracking Across Generations\n")

for result in results:
    print(f"\n{result['Crossover Type']} Crossover - Generation Statistics:")
    print("{:<12} {:<15} {:<15} {:<15} {:<12} {:<12} {:<12}".format(
        "Generation", "Best Cost", "Worst Cost", "Avg Cost", "Total", "Mutated", "Not Mutated"))
    print("-" * 100)
    
    for stat in result['Generation Stats']:
        print("{:<12} {:<15} {:<15} {:<15.2f} {:<12} {:<12} {:<12}".format(
            stat['Generation'],
            stat['Best Child Cost'],
            stat['Worst Child Cost'],
            stat['Avg Child Cost'],
            stat['Total Children'],
            stat['Mutated'],
            stat['Not Mutated']
        ))

# Display comparison of mutation patterns
print("\n" + "="*100)
print("MUTATION PATTERN COMPARISON - One Point vs Two Point Crossover\n")

print("Sample Generations Showing Mutation Differences:\n")
print("{:<12} {:<20} {:<15} {:<15} {:<20} {:<15} {:<15}".format(
    "Generation", "Crossover Type", "Mutated", "Not Mutated", "Mutation Rate %", "Best Cost", "Avg Cost"))
print("-" * 110)

# Show mutations for every 50th generation
for gen_idx in [0, 49, 99, 149, 199]:  # First, 50th, 100th, 150th, 200th
    for result in results:
        if gen_idx < len(result['Generation Stats']):
            stat = result['Generation Stats'][gen_idx]
            mutation_rate = (stat['Mutated'] / stat['Total Children'] * 100) if stat['Total Children'] > 0 else 0
            print("{:<12} {:<20} {:<15} {:<15} {:<20.1f} {:<15} {:<15.2f}".format(
                stat['Generation'],
                result['Crossover Type'],
                stat['Mutated'],
                stat['Not Mutated'],
                mutation_rate,
                stat['Best Child Cost'],
                stat['Avg Child Cost']
            ))
    print()


print()