import heapq

# Cities in order (14 cities total)
cities = [
    "Chicago", "Detroit", "Cleveland", "Indianapolis", "Columbus",
    "Pittsburgh", "Buffalo", "Syracuse", "Boston", "Portland",
    "Providence", "New York", "Philadelphia", "Baltimore"
]

# Heuristic values h(n) - distance to Boston (miles)
h = {
    "Boston": 0,
    "Providence": 50,
    "Portland": 107,
    "New York": 215,
    "Philadelphia": 270,
    "Baltimore": 360,
    "Syracuse": 260,
    "Buffalo": 400,
    "Pittsburgh": 470,
    "Cleveland": 550,
    "Columbus": 640,
    "Detroit": 610,
    "Indianapolis": 780,
    "Chicago": 860
}

# Adjacency Matrix with actual distances (14x14)
# Order: Chicago, Detroit, Cleveland, Indianapolis, Columbus, Pittsburgh, Buffalo, Syracuse, Boston, Portland, Providence, New York, Philadelphia, Baltimore
distance = [
#Ch De Cl In Co  P  Bu Sy Bo Po Pr NY Ph Ba
[0, 283, 345, 182, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     # Chicago (0)
[283, 0, 169, 0, 0, 0, 256, 0, 0, 0, 0, 0, 0, 0],     # Detroit (1)
[345, 169, 0, 0, 144, 134, 189, 0, 0, 0, 0, 0, 0, 0], # Cleveland (2)
[182, 0, 0, 0, 176, 0, 0, 0, 0, 0, 0, 0, 0, 0],       # Indianapolis (3)
[0, 0, 144, 176, 0, 185, 0, 0, 0, 0, 0, 0, 0, 0],     # Columbus (4)
[0, 0, 134, 0, 185, 0, 215, 0, 0, 0, 0, 0, 305, 247], # Pittsburgh (5)
[0, 256, 189, 0, 0, 215, 0, 150, 0, 0, 0, 0, 0, 0],   # Buffalo (6)
[0, 0, 0, 0, 0, 0, 150, 0, 312, 0, 0, 254, 253, 0],   # Syracuse (7)
[0, 0, 0, 0, 0, 0, 0, 312, 0, 107, 50, 215, 0, 0],    # Boston (8)
[0, 0, 0, 0, 0, 0, 0, 0, 107, 0, 0, 0, 0, 0],         # Portland (9)
[0, 0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 181, 0, 0],        # Providence (10)
[0, 0, 0, 0, 0, 0, 0, 254, 215, 0, 181, 0, 97, 0],    # New York (11)
[0, 0, 0, 0, 0, 305, 0, 253, 0, 0, 0, 97, 0, 101],    # Philadelphia (12)
[0, 0, 0, 0, 0, 247, 0, 0, 0, 0, 0, 0, 101, 0]        # Baltimore (13)
]

# Greedy Best First Search
def greedy_best_first(start, goal):
    pq = [(h[start], start, [start], 0)]  # (heuristic, city, path, cost)
    visited = set()
    explored_order = []

    while pq:
        heuristic, city, path, cost = heapq.heappop(pq)

        if city in visited:
            continue

        visited.add(city)
        explored_order.append(city)

        if city == goal:
            return path, cost, explored_order

        city_idx = cities.index(city)

        for j in range(len(distance)):
            if distance[city_idx][j] > 0:
                neighbor = cities[j]
                if neighbor not in visited:
                    heapq.heappush(pq, (h[neighbor], neighbor, path + [neighbor], cost + distance[city_idx][j]))

    return None, float('inf'), explored_order

# A* Algorithm
def astar_search(start, goal):
    pq = [(h[start], 0, start, [start])]  # (f=g+h, g, city, path)
    visited = set()
    explored_order = []

    while pq:
        f_score, g_cost, city, path = heapq.heappop(pq)

        if city in visited:
            continue

        visited.add(city)
        explored_order.append(city)

        if city == goal:
            return path, g_cost, explored_order

        city_idx = cities.index(city)

        for j in range(len(distance)):
            if distance[city_idx][j] > 0:
                neighbor = cities[j]
                if neighbor not in visited:
                    new_g = g_cost + distance[city_idx][j]
                    f = new_g + h[neighbor]
                    heapq.heappush(pq, (f, new_g, neighbor, path + [neighbor]))

    return None, float('inf'), explored_order

# Run searches
start = "Chicago"
goal = "Boston"

gbfs_path, gbfs_cost, gbfs_explored = greedy_best_first(start, goal)
astar_path, astar_cost, astar_explored = astar_search(start, goal)

print("GREEDY BEST FIRST SEARCH")
print(f"Path: {' → '.join(gbfs_path)}")
print(f"Cost: {gbfs_cost}, Cities Explored: {len(gbfs_explored)}")

print("\nA* SEARCH")
print(f"Path: {' → '.join(astar_path)}")
print(f"Cost: {astar_cost}, Cities Explored: {len(astar_explored)}")

print("\nCOMPARISON")
print(f"GBFS: {len(gbfs_explored)} cities | A*: {len(astar_explored)} cities")
