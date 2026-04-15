# Lab 9.2: Extend Lab 1 - Alpha-Beta Pruning on City Map Graph
# Compare efficiency gains and analyze pruning patterns on varied game trees

from collections import deque

# City graph with distances
graph = {
    'Chicago': [('Detroit', 283), ('Indianapolis', 182), ('Cleveland', 345)],
    'Detroit': [('Chicago', 283), ('Buffalo', 256), ('Cleveland', 169)],
    'Buffalo': [('Detroit', 256), ('Syracuse', 150), ('Cleveland', 189)],
    'Syracuse': [('Buffalo', 150), ('Boston', 312), ('New York', 150)],
    'Boston': [('Syracuse', 312), ('Providence', 50), ('New York', 107)],
    'Providence': [('Boston', 50), ('New York', 181)],
    'New York': [('Syracuse', 150), ('Boston', 107), ('Providence', 181), ('Philadelphia', 97)],
    'Philadelphia': [('New York', 97), ('Pittsburgh', 305), ('Baltimore', 101)],
    'Baltimore': [('Philadelphia', 101), ('Pittsburgh', 247)],
    'Pittsburgh': [('Philadelphia', 305), ('Buffalo', 189), ('Cleveland', 134), ('Columbus', 185), ('Baltimore', 247)],
    'Cleveland': [('Detroit', 169), ('Buffalo', 189), ('Pittsburgh', 134), ('Columbus', 144), ('Chicago', 345)],
    'Columbus': [('Cleveland', 144), ('Pittsburgh', 185), ('Indianapolis', 176)],
    'Indianapolis': [('Chicago', 182), ('Columbus', 176)],
}

nodes_bfs = 0
nodes_dfs = 0
nodes_ab = 0


# ============= BFS IMPLEMENTATION =============

def bfs_shortest_path(start, end, graph):
    """Find shortest path using BFS"""
    global nodes_bfs
    nodes_bfs = 0
    
    queue = deque([(start, [start], 0)])
    visited = set()
    
    while queue:
        node, path, cost = queue.popleft()
        nodes_bfs += 1
        
        if node == end:
            return path, cost
        
        if node in visited:
            continue
        visited.add(node)
        
        if node in graph:
            for neighbor, distance in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor], cost + distance))
    
    return None, float('inf')


# ============= DFS IMPLEMENTATION =============

def dfs_shortest_path(start, end, graph):
    """Find shortest path using DFS"""
    global nodes_dfs
    nodes_dfs = 0
    
    def dfs(node, end, path, cost, visited):
        global nodes_dfs
        nodes_dfs += 1
        
        if node == end:
            return path, cost
        
        visited.add(node)
        best_path = None
        best_cost = float('inf')
        
        if node in graph:
            for neighbor, distance in graph[node]:
                if neighbor not in visited:
                    new_visited = visited.copy()
                    result_path, result_cost = dfs(neighbor, end, path + [neighbor], cost + distance, new_visited)
                    
                    if result_path and result_cost < best_cost:
                        best_path = result_path
                        best_cost = result_cost
        
        return best_path, best_cost
    
    return dfs(start, end, [start], 0, set())


# ============= ALPHA-BETA PRUNING FOR GRAPH SEARCH =============

def alpha_beta_pruning(start, end, graph, alpha=0, beta=float('inf')):
    """Alpha-Beta pruning finds optimal path by pruning expensive branches"""
    global nodes_ab
    nodes_ab = 0
    best_path = None
    best_cost = float('inf')
    
    def search(node, path, cost, alpha, beta, visited):
        global nodes_ab
        nodes_ab += 1
        nonlocal best_path, best_cost
        
        # Pruning: if cost already exceeds current best, abandon this path
        if cost >= beta:
            return None, beta
        
        if node == end:
            if cost < best_cost:
                best_cost = cost
                best_path = path
            return path, cost
        
        visited.add(node)
        
        # Sort neighbors by distance (good move ordering improves pruning)
        if node in graph:
            neighbors = sorted(graph[node], key=lambda x: x[1])
            
            for neighbor, distance in neighbors:
                if neighbor not in visited:
                    new_cost = cost + distance
                    
                    # Pruning: skip if already worse than best found
                    if new_cost >= beta:
                        continue
                    
                    result_path, result_cost = search(neighbor, path + [neighbor], new_cost, alpha, beta, visited.copy())
                    
                    if result_path and result_cost < beta:
                        beta = result_cost
        
        return best_path, best_cost
    
    search(start, [start], 0, alpha, beta, set())
    return best_path, best_cost


# ============= ANALYSIS ON VARIED GAME TREES =============

def analyze_route(start, end, scenario_name):
    """Analyze efficiency across algorithms for a route"""
    print(f"\n{scenario_name}: {start} → {end}")
    print("-" * 60)
    
    # BFS
    path_bfs, cost_bfs = bfs_shortest_path(start, end, graph)
    print(f"BFS:")
    print(f"  Path: {' → '.join(path_bfs) if path_bfs else 'Not found'}")
    print(f"  Cost: {cost_bfs} miles")
    print(f"  Nodes expanded: {nodes_bfs}")
    
    # DFS
    path_dfs, cost_dfs = dfs_shortest_path(start, end, graph)
    print(f"\nDFS:")
    print(f"  Path: {' → '.join(path_dfs) if path_dfs else 'Not found'}")
    print(f"  Cost: {cost_dfs} miles")
    print(f"  Nodes expanded: {nodes_dfs}")
    
    # Alpha-Beta Pruning
    path_ab, cost_ab = alpha_beta_pruning(start, end, graph)
    print(f"\nAlpha-Beta Pruning:")
    print(f"  Path: {' → '.join(path_ab) if path_ab else 'Not found'}")
    print(f"  Cost: {cost_ab} miles")
    print(f"  Nodes expanded: {nodes_ab}")
    
    # Efficiency comparison
    print(f"\nEfficiency Gains:")
    if nodes_bfs > 0:
        bfs_reduction = ((nodes_bfs - nodes_ab) / nodes_bfs) * 100
        print(f"  BFS reduction: {bfs_reduction:.1f}%")
    
    if nodes_dfs > 0:
        dfs_reduction = ((nodes_dfs - nodes_ab) / nodes_dfs) * 100
        print(f"  DFS reduction: {dfs_reduction:.1f}%")
    
    return nodes_bfs, nodes_dfs, nodes_ab


# ============= MAIN EXECUTION =============

print("\n" + "="*70)
print("LAB 9.2: ALPHA-BETA PRUNING ON CITY MAP")
print("Extend Lab 1 with efficiency analysis across varied game trees")
print("="*70)

# Scenario 1: Short routes (shallow trees)
print("\n" + "="*70)
print("SCENARIO 1: SHORT ROUTES (Shallow Search Trees)")
print("="*70)

m1, d1, ab1 = analyze_route('Boston', 'New York', "Short route: Limited options")

# Scenario 2: Medium routes (medium depth trees)
print("\n" + "="*70)
print("SCENARIO 2: MEDIUM ROUTES (Medium Depth Trees)")
print("="*70)

m2, d2, ab2 = analyze_route('Syracuse', 'Chicago', "Medium route: Moderate branching")

# Scenario 3: Long routes (deep trees)
print("\n" + "="*70)
print("SCENARIO 3: LONG ROUTES (Deep Search Trees)")
print("="*70)

m3, d3, ab3 = analyze_route('Boston', 'Indianapolis', "Long route: Maximum branching")

# ============= PRUNING PATTERNS ANALYSIS =============

print("\n" + "="*70)
print("PRUNING PATTERNS ANALYSIS - VARIED GAME TREES")
print("="*70)

scenarios = [
    ("Short Route", m1, d1, ab1),
    ("Medium Route", m2, d2, ab2),
    ("Long Route", m3, d3, ab3)
]

print("\n{:<20} {:<12} {:<12} {:<12}".format("Scenario", "BFS", "DFS", "Alpha-Beta"))
print("-" * 60)

for name, bfs, dfs, ab in scenarios:
    print("{:<20} {:<12} {:<12} {:<12}".format(name, str(bfs), str(dfs), str(ab)))

print("\n" + "="*70)

print("• Pruning efficiency vs DFS:")
dfs_reductions = []
for name, bfs, dfs, ab in scenarios:
    if dfs > 0:
        reduction = ((dfs - ab) / dfs) * 100
        dfs_reductions.append(reduction)
        print(f"  {name}: {reduction:.1f}%")
avg_reduction = sum(dfs_reductions) / len(dfs_reductions) if dfs_reductions else 0
print(f"  Average: {avg_reduction:.1f}%")
print("="*70 + "\n")