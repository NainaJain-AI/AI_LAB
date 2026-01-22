

def create_queue():
    return []

def enqueue(queue, item):
    queue.append(item)

def dequeue(queue):
    if not is_queue_empty(queue):
        return queue.pop(0)
    return None

def is_queue_empty(queue):
    return len(queue) == 0

graph = {
    "Syracuse": [("Buffalo",150), ("Pittsburgh",253), ("New York",254), ("Boston",312)],
    "Buffalo": [("Detroit",256), ("Cleveland",189), ("Syracuse",150)],
    "Pittsburgh": [("Cleveland",134), ("Columbus",185), ("Baltimore",247), ("Philadelphia",305), ("Syracuse",253)],
    "Cleveland": [("Chicago",345), ("Detroit",169), ("Columbus",144), ("Buffalo",189), ("Pittsburgh",134)],
    "Columbus": [("Cleveland",144), ("Indianapolis",176), ("Pittsburgh",185)],
    "Detroit": [("Chicago",283), ("Cleveland",169), ("Buffalo",256)],
    "Chicago": [("Detroit",283), ("Cleveland",345), ("Indianapolis",182)],
    "Indianapolis": [("Chicago",182), ("Columbus",176)],
    "New York": [("Philadelphia",97), ("Boston",215), ("Providence",181), ("Syracuse",254)],
    "Philadelphia": [("New York",97), ("Baltimore",101), ("Pittsburgh",305)],
    "Baltimore": [("Philadelphia",101), ("Pittsburgh",247)],
    "Boston": [("New York",215), ("Providence",50), ("Portland",107), ("Syracuse",312)],
    "Providence": [("Boston",50), ("New York",181)],
    "Portland": [("Boston",107)]
}

def bfs_all_paths_with_exploration(graph, start, goal):
    print("\nBFS – ALL PATHS WITH TOTAL COST (PATH + EXPLORATION)\n")

    queue = []
    queue.append((start, [start], 0, 0))
    # (current_city, path, path_cost, exploration_cost)

    results = []

    while queue:
        city, path, path_cost, exploration_cost = queue.pop(0)

        # Exploration cost for expanding this node
        node_exploration = 0
        for neighbor, step_cost in graph.get(city, []):
            node_exploration += step_cost

        new_exploration_cost = exploration_cost + node_exploration

        if city == goal:
            total_cost = path_cost + new_exploration_cost
            results.append((path, path_cost, new_exploration_cost, total_cost))
            continue

        for neighbor, step_cost in graph.get(city, []):
            if neighbor not in path:
                queue.append(
                    (neighbor,
                     path + [neighbor],
                     path_cost + step_cost,
                     new_exploration_cost)
                )

    for i, r in enumerate(results, 1):
        p, pc, ec, tc = r
        print(f"Path {i}: {' -> '.join(p)}")
        print(f"  Path Cost        = {pc}")
        print(f"  Exploration Cost = {ec}")
        print(f"  TOTAL COST       = {tc}\n")

    print("Total paths found (BFS):", len(results))



def dfs_all_paths_with_exploration(graph, start, goal):
    print("\nDFS – ALL PATHS WITH TOTAL COST (PATH + EXPLORATION)\n")

    stack = [(start, [start], 0, 0)]
    results = []

    while stack:
        city, path, path_cost, exploration_cost = stack.pop()

        node_exploration = 0
        for neighbor, step_cost in graph.get(city, []):
            node_exploration += step_cost

        new_exploration_cost = exploration_cost + node_exploration

        if city == goal:
            total_cost = path_cost + new_exploration_cost
            results.append((path, path_cost, new_exploration_cost, total_cost))
            continue

        for neighbor, step_cost in graph.get(city, []):
            if neighbor not in path:
                stack.append(
                    (neighbor,
                     path + [neighbor],
                     path_cost + step_cost,
                     new_exploration_cost)
                )

    for i, r in enumerate(results, 1):
        p, pc, ec, tc = r
        print(f"Path {i}: {' -> '.join(p)}")
        print(f"  Path Cost        = {pc}")
        print(f"  Exploration Cost = {ec}")
        print(f"  TOTAL COST       = {tc}\n")

    print("Total paths found (DFS):", len(results))


bfs_all_paths_with_exploration(graph, "Syracuse", "Chicago")
dfs_all_paths_with_exploration(graph, "Syracuse", "Chicago")



