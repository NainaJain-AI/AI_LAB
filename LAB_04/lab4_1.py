import heapq

cities = [
"Chicago","Detroit","Cleveland","Indianapolis","Columbus",
"Pittsburgh","Buffalo","Syracuse","Boston","Portland",
"Providence","New York","Philadelphia","Baltimore"
]

M = [
[0,283,345,182,0,0,0,0,0,0,0,0,0,0],
[283,0,169,0,0,0,256,0,0,0,0,0,0,0],
[345,169,0,0,144,134,189,0,0,0,0,0,0,0],
[182,0,0,0,176,0,0,0,0,0,0,0,0,0],
[0,0,144,176,0,185,0,0,0,0,0,0,0,0],
[0,0,134,0,185,0,215,0,0,0,0,0,305,247],
[0,256,189,0,0,215,0,150,0,0,0,0,0,0],
[0,0,0,0,0,0,150,0,312,0,0,254,253,0],
[0,0,0,0,0,0,0,312,0,107,50,215,0,0],
[0,0,0,0,0,0,0,0,107,0,0,0,0,0],
[0,0,0,0,0,0,0,0,50,0,0,181,0,0],
[0,0,0,0,0,0,0,254,215,0,181,0,97,0],
[0,0,0,0,0,305,0,253,0,0,0,97,0,101],
[0,0,0,0,0,247,0,0,0,0,0,0,101,0]
]

def UCS(start, goal):
    n = len(M)
    pq = [(0, start, [start])]
    visited = [False]*n
    explored = 0

    while pq:
        cost, node, path = heapq.heappop(pq)
        
        if visited[node]:
            continue
        
        visited[node] = True
        explored += 1

        if node == goal:
            return path, cost, explored

        for j in range(n):
            if M[node][j] > 0 and not visited[j]:
                heapq.heappush(pq, (cost + M[node][j], j, path+[j]))

start = 7   # Syracuse
goal = 0    # Chicago

path, cost, explored = UCS(start, goal)

print("Path:", " -> ".join(cities[i] for i in path))
print("Total Distance:", cost)
print(" Unique Nodes Explored:", explored)