import heapq

floor = [
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1],
    [1,1,0,1,1,1,1,1],
    [1,1,0,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
]

rows = len(floor)
cols = len(floor[0])

start = (4, 2)
goal = (2, 6)

def ucs_grid():
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, (r, c), path = heapq.heappop(pq)

        if (r, c) == goal:
            return path, cost

        if (r, c) not in visited:
            visited.add((r, c))

            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dr, dc in moves:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if floor[nr][nc] == 0 and (nr, nc) not in visited:
                        new_cost = cost + 1
                        new_path = path + [(nr, nc)]
                        heapq.heappush(pq, (new_cost, (nr, nc), new_path))

    return None

result = ucs_grid()

if result:
    path, steps = result
    print("Path Visualization:")
    for idx, pos in enumerate(path):
        if idx == 0:
            print(f"{pos} ← START")
        elif idx == len(path) - 1:
            print(f"{pos} ← GOAL (EXIT)")
        else:
            print(f"{pos}")
    
    print(f"\nTotal Cost: {steps}")
    
    print("\nPath visualization on grid:")
    grid_display = [row[:] for row in floor]
    for r, c in path:
        if grid_display[r][c] == 0:
            grid_display[r][c] = '*'
    
    for r_idx, row in enumerate(grid_display):
        row_display = []
        for c_idx, cell in enumerate(row):
            if (r_idx, c_idx) == start:
                row_display.append('S')
            elif (r_idx, c_idx) == goal:
                row_display.append('E')
            elif cell == '*':
                row_display.append('*')
            elif cell == 0:
                row_display.append('.')
            else:
                row_display.append('#')
        print(' '.join(row_display))
else:
    print("No path found")