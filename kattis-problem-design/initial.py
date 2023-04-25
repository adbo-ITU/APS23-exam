from sys import stdin
from collections import defaultdict, deque

r, c, b = [int(x) for x in next(stdin).split()]

graph = defaultdict(lambda: defaultdict(int))
rows = [[False for _ in range(c)] for _ in range(r)]

# Read input
for row in range(r):
    chars = list(next(stdin).strip())

    for col in range(c):
        if chars[col] == "#":
            rows[row][col] = True


# Construct graph
for row in range(r - 1):
    for col in range(c):
        if rows[row][col]:
            for dx in [-1, 0, 1]:
                x, y = col + dx, row + 1

                if x < 0 or x >= c:
                    continue

                if rows[y][x]:
                    graph[(row, col)][(y, x)] = 1

# Add source and sink
source, sink = (-1, 0), (-1, 1)  # ensure outside of grid
for col in range(c):
    if rows[0][col]:
        graph[source][(0, col)] = 1

    if rows[r - 1][col]:
        graph[(r - 1, col)][sink] = 1

# Print all edges in the graph
# for start, adj in graph.items():
#     for end, weight in adj.items():
#         print(start, end, weight)


# Find max flow
def bfs(graph, source, sink, min_capacity=0):
    parent = dict()
    queue = deque([source])

    while queue:
        u = queue.popleft()

        for v, capacity in graph[u].items():
            if capacity > min_capacity and v not in parent:
                parent[v] = u
                queue.append(v)

                if v == sink:
                    path = []
                    cur = sink
                    while source != cur:
                        prev = parent[cur]
                        path.append((prev, cur))
                        cur = prev

                    return (True, path)

    return (False, set(parent))


def find_max_flow(original_graph, source, sink):
    graph = defaultdict(lambda: defaultdict(lambda: 0))
    max_capacity = 0

    for u, d in original_graph.items():
        for v, c in d.items():
            graph[u][v] = c
            max_capacity = max(max_capacity, c)

    current_flow = 0
    min_capacity = max_capacity
    while True:
        has_path, path = bfs(graph, source, sink, min_capacity)

        if not has_path:
            if min_capacity <= 0:
                return current_flow

            min_capacity //= 2
            continue

        path_flow = min(graph[u][v] for u, v in path)
        current_flow += path_flow

        for u, v in path:
            graph[u][v] -= path_flow
            graph[v][u] += path_flow


max_flow = find_max_flow(graph, source, sink)

print(b - max_flow)
