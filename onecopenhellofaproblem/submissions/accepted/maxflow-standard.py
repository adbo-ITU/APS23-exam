#!/usr/bin/env python3

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


in_flag, out_flag = 0, 1

# Construct graph
for row in range(r):
    for col in range(c):
        if rows[row][col]:
            # Add edge from node's own in-node to its out-node
            graph[(row, col, in_flag)][(row, col, out_flag)] = 1

            # Add all possible edges to adjacent nodes' in-nodes
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    x, y = col + dx, row + dy

                    if x < 0 or x >= c or y >= r or y < 0:
                        continue

                    if rows[y][x]:
                        graph[(row, col, out_flag)][(y, x, in_flag)] = 1

# Add source and sink
source, sink = (-1, 0, out_flag), (-1, 1, in_flag)  # ensure outside of grid
for col in range(c):
    if rows[0][col]:
        graph[source][(0, col, in_flag)] = 1

    if rows[r - 1][col]:
        graph[(r - 1, col, out_flag)][sink] = 1


INF = float("Inf")

def find_max_flow():
    max_flow = 0

    while True:
        parent = flow_bfs(source, sink)

        if parent is None:
            break

        flow = INF

        cur = sink
        while cur != source:
            p = parent[cur]
            flow = min(flow, graph[p][cur])
            cur = p

        cur = sink
        while cur != source:
            p = parent[cur]
            graph[p][cur] -= flow
            graph[cur][p] += flow
            cur = p

        max_flow += flow

    return max_flow


def flow_bfs(s, t):
    visited = set()
    parent = dict()
    queue = deque([s])
    visited.add(s)

    while queue:
        cur = queue.popleft()

        for n in graph[cur]:
            if not n in visited and graph[cur][n] > 0:
                queue.append(n)
                parent[n] = cur
                visited.add(n)

                if n == t:
                    return parent

    return None

max_flow = find_max_flow()

remaining = max(0, b - max_flow)

print(remaining)
