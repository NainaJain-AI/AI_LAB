TOTAL_G = 3
TOTAL_B = 3

def is_valid(g_left, b_left):
    g_right = TOTAL_G - g_left
    b_right = TOTAL_B - b_left

    if g_left < 0 or b_left < 0 or g_left > 3 or b_left > 3:
        return False

    # Girls not outnumbered
    if g_left > 0 and b_left > g_left:
        return False
    if g_right > 0 and b_right > g_right:
        return False

    return True

def get_children(state):
    g, b, boat = state
    moves = [(1,0),(0,1),(2,0),(0,2),(1,1)]
    children = []

    for mg, mb in moves:
        if boat == 'L':
            new_g = g - mg
            new_b = b - mb
            new_boat = 'R'
        else:
            new_g = g + mg
            new_b = b + mb
            new_boat = 'L'

        if is_valid(new_g, new_b):
            children.append((new_g, new_b, new_boat))

    return children

def dls(state, goal, limit, path, visited, explored, initial_limit=None):
    if initial_limit is None:
        initial_limit = limit
    
    current_depth = initial_limit - limit
    g, b, boat = state
    
    if state == goal:
        return path, explored

    if limit == 0:
        return None, explored

    visited.add(state)
    explored.append((g, b, boat, current_depth))

    for child in get_children(state):
        if child not in visited:
            result, explored = dls(child, goal, limit-1, path + [child], visited, explored, initial_limit)
            if result is not None:
                return result, explored

    return None, explored

def ids(start, goal):
    depth = 0
    while True:
        visited = set()
        result, explored = dls(start, goal, depth, [start], visited, [])
        if result is not None:
            return result, explored
        depth += 1

def print_path(path):
    for g, b, boat in path:
        g_right = TOTAL_G - g
        b_right = TOTAL_B - b
        print(f"G:{g} B:{b} | G:{g_right} B:{b_right}, Boat: {'Left' if boat == 'L' else 'Right'}")

def print_explored(explored):
    print("States Explored:")
    for g, b, boat, depth in explored:
        g_right = TOTAL_G - g
        b_right = TOTAL_B - b
        print(f"  G:{g} B:{b} | G:{g_right} B:{b_right}, Boat: {'Left' if boat == 'L' else 'Right'}, Depth: {depth}")

start = (3, 3, 'L')
goal = (0, 0, 'R')

print("Depth Limited Search (limit=3):")
res, explored_dls = dls(start, goal, 3, [start], set(), [])
print_explored(explored_dls)
if res is None:
    print("Cutoff / No solution within depth 3")
else:
    print("\nPath Found:")
    print_path(res)

print("\n" + "="*50)
print("Iterative Deepening Search:")
solution, explored_ids = ids(start, goal)
print_explored(explored_ids)
print("\nPath Found:")
print_path(solution)