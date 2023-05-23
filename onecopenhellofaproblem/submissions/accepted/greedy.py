#!/usr/bin/env python3

import sys

# Default recursion limit will be exceeded given worst-case input
sys.setrecursionlimit(1_000_000)

# Read input
r, c, b = map(int, input().split())
grid = [[cell == '#' for cell in input()] for _ in range(r)]
visited = [[False] * c for _ in range(r)]
directions = [
    (1, 0),    # Down
    (1, 1),    # Down right
    (0, 1),    # Right
    (-1, 1),   # Up right
    (-1, 0),   # Up
    (-1, -1),  # Up left
    (0, -1),   # Left
    (1, -1),   # Down left
]


def left_turn(direction, steps=1):
    return (direction + steps) % 8


def greedy_search(row, col, direction=0):
    # Out of bounds
    if row < 0 or row >= r or col < 0 or col >= c:
        return False
    # Already visited or not traversable
    if visited[row][col] or not grid[row][col]:
        return False

    visited[row][col] = True

    # Path found
    if row == r - 1:
        return True

    # 180-degree turn
    direction = left_turn(direction, steps=4)

    # Then explore all directions in a counter-clockwise manner
    for _ in directions:
        direction = left_turn(direction)
        dy, dx = directions[direction]

        if greedy_search(row + dy, col + dx, direction):
            return True

    return False


# Start search from each entry cell in the top row
paths = sum(1 if greedy_search(0, i) else 0 for i in range(c))
print(max(0, b - paths))
