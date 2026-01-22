
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0



def to_tuple(state):
    return (
        tuple(state[0]),
        tuple(state[1]),
        tuple(state[2])
    )


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)

    moves = [(-1,0), (1,0), (0,-1), (0,1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [
                state[0][:],
                state[1][:],
                state[2][:]
            ]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors


#  BFS 
def bfs(start, goal):
    queue = Queue()
    queue.enqueue(start)

    visited = set()        
    visited.add(to_tuple(start))

    explored = 0

    while not queue.is_empty():
        current = queue.dequeue()
        explored += 1

        if current == goal:
            return explored

        for neighbor in get_neighbors(current):
            t = to_tuple(neighbor)
            if t not in visited:
                visited.add(t)
                queue.enqueue(neighbor)

    return -1


# ---------------- MAIN ----------------
start_state = [
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
]

goal_state = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

result = bfs(start_state, goal_state)
print("Number of states explored before reaching goal:", result)
