#!/usr/bin/env python3

from collections import defaultdict


graph = defaultdict(list)


def add_edge(u, v):
    graph[u].append(v)


r, c, b = [int(x) for x in input().split()]

rows = [[False for _ in range(c)] for _ in range(r)]

# Read input
for row in range(r):
    chars = list(input().strip())

    for col in range(c):
        if chars[col] == "#":
            rows[row][col] = True

for row in range(r):
    for col in range(c):
        if rows[row][col]:
            # Add all possible edges to adjacent nodes' in-nodes
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    x, y = col + dx, row + dy

                    if x < 0 or x >= c or y >= r or y < 0:
                        continue

                    if rows[y][x]:
                        # graph[(row, col)][(y, x)] = 1
                        add_edge((row, col), (y, x))


# Add source and sink
source, sink = (-1, 0), (-1, 1)  # ensure outside of grid
for col in range(c):
    if rows[0][col]:
        add_edge(source, (0, col))

    if rows[r - 1][col]:
        add_edge((r - 1, col), sink)


visited = set()
path = []
all_paths = []


def add_all_paths(u, d):
    if u == d:
        all_paths.append(path.copy())
    else:
        visited.add(u)

        if u != source:
            path.append(u)

        for i in graph[u]:
            if i not in visited:
                add_all_paths(i, d)

        if len(path):
            path.pop()
        visited.remove(u)


add_all_paths(source, sink)

paths = [set(p) for p in all_paths]

combs = [[p] for p in paths]

for p in paths:
    for c in combs:
        if all(p.isdisjoint(i) for i in c):
            c.append(p)

max_carry = max(len(c) for c in combs) if len(combs) else 0
remaining = max(0, b - max_carry)

print(remaining)
