import heapq
from itertools import permutations

"""
MAZE SOLVER WITH A* ALGORITHM
==============================
Maze: 5x5 matrix
  0 = empty tile (walkable)
  1 = wall (obstacle)
  2 = start position
  3 = reward (goal)

Goal: Visit ALL rewards using A* algorithm

Heuristic: h(n) = Manhattan Distance
  h(n) = |current_row - goal_row| + |current_col - goal_col|
  Justification: Never overestimates, admissible for A*

Evaluation Cost: g(n) = steps taken  
  g(n) = number of moves (each = 1 unit)
  Justification: Equal cost per move in grid
"""

maze = [
    [2,0,0,0,1],    # Row 0
    [0,1,0,0,3],    # Row 1
    [0,3,0,1,1],    # Row 2
    [0,1,0,0,1],    # Row 3
    [3,0,0,0,3]     # Row 4
]

ROWS = 5
COLS = 5

start = None
rewards = []

for r in range(ROWS):
    for c in range(COLS):
        if maze[r][c] == 2:
            start = (r, c)
        if maze[r][c] == 3:
            rewards.append((r, c))

def heuristic(a, b):
    """Manhattan distance - never overestimates, admissible heuristic"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(r, c):
    """Get valid neighbors (not walls, within bounds)"""
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
            result.append((nr, nc))
    
    return result

def astar(start_pos, goal_pos):
    """A* pathfinding: f(n) = g(n) + h(n)"""
    pq = [(heuristic(start_pos, goal_pos), 0, start_pos)]
    g_cost = {start_pos: 0}
    parent = {}
    visited = set()
    visited_order = []

    while pq:
        f_cost, g, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == goal_pos:
            path = []
            node = current
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start_pos)
            path.reverse()
            return path, visited_order

        for neighbor in get_neighbors(*current):
            if neighbor not in visited:
                new_g = g_cost[current] + 1

                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    g_cost[neighbor] = new_g
                    f = new_g + heuristic(neighbor, goal_pos)
                    heapq.heappush(pq, (f, new_g, neighbor))
                    parent[neighbor] = current

    return None, visited_order

def find_optimal_tour():
    """Find optimal order to visit all rewards"""
    best_path = []
    best_visited = []
    min_cost = float('inf')

    for reward_order in permutations(rewards):
        total_path = [start]
        total_visited = []
        current = start
        total_cost = 0

        for reward in reward_order:
            path, visited = astar(current, reward)
            if path is None:
                total_cost = float('inf')
                break

            total_path.extend(path[1:])
            total_visited.extend(visited)
            total_cost += len(path) - 1
            current = reward

        if total_cost < min_cost:
            min_cost = total_cost
            best_path = total_path
            best_visited = total_visited

    return best_path, best_visited, min_cost

print("Start: {0}, Rewards: {1}\n".format(start, rewards))

path, visited, cost = find_optimal_tour()

if path:
    print("Path: {0}".format(' → '.join([str(p) for p in path])))
    print("Cost: {0}\n".format(cost))
    
    print("Maze (S=start, R=reward, #=wall, *=path):")
    display = [row[:] for row in maze]
    
    for pos in path:
        r, c = pos
        if display[r][c] == 0:
            display[r][c] = '*'
    
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            if (r, c) == start:
                row_str += "S "
            elif (r, c) in rewards:
                row_str += "R "
            elif display[r][c] == '*':
                row_str += "* "
            elif display[r][c] == 1:
                row_str += "# "
            else:
                row_str += ". "
        print(row_str)
else:
    print("No path found")
