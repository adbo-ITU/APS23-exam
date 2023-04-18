from sys import stdin
from collections import defaultdict

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
source, sink = (-1, 0), (-1, 1) # ensure outside of grid
for col in range(c):
    if rows[0][col]:
        graph[source][(0, col)] = 1

    if rows[r - 1][col]:
        graph[(r - 1, col)][sink] = 1

# Print all edges in the graph
for start, adj in graph.items():
    for end, weight in adj.items():
        print(start, end, weight)
