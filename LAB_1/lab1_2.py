class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0
graph = {
    "Raj": ["Priya", "Akash", "Sunil"],
    "Priya": ["Raj", "Aarav", "Neha1"],
    "Aarav": ["Priya", "Neha2", "Arjun1"],

    "Sunil": ["Raj", "Akash", "Sneha"],
    "Akash": ["Raj", "Sunil", "Neha1"],

    "Neha1": ["Priya", "Akash", "Rahul"],
    "Neha2": ["Aarav", "Rahul"],

    "Sneha": ["Sunil", "Rahul", "Maya"],
    "Rahul": ["Neha1", "Neha2", "Sneha", "Pooja", "Arjun1"],

    "Maya": ["Sneha", "Arjun2"],

    "Arjun1": ["Aarav", "Rahul", "Pooja"],
    "Arjun2": ["Maya", "Pooja"],

    "Pooja": ["Rahul", "Arjun1", "Arjun2"]
}
def bfs(graph, start):
    visited = []
    q = Queue()

    visited.append(start)
    q.enqueue(start)

    while not q.is_empty():
        node = q.dequeue()
        print(node, end=" ")

        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.append(neighbour)
                q.enqueue(neighbour)


def dfs(graph, node, visited=None):
    if visited is None:
        visited = []

    visited.append(node)
    print(node, end=" ")

    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs(graph, neighbour, visited)

print("BFS Traversal:")
bfs(graph, "Raj")            
print("\nDFS Traversal:")
dfs(graph, "Raj")

