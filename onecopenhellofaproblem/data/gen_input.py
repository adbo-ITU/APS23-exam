#!/usr/bin/python3

import random


def generate_bottleneck_input(rows, columns, band_members):
    """
    Randomly generates a grid with (columns/4) paths, limited by a bottleneck in the following format:

    5 8 5
    .#.##..#
    #..#.#.#
    .#...#..  <-- bottleneck
    .##..##.
    .#.##..#
    """

    grid = [['.' for _ in range(columns)] for _ in range(rows)]
    for i, row in enumerate(grid):
        for j in range(0, len(row) - 1, 4 if i == len(grid) // 2 else 2):
            row[j + random.randint(0, 1)] = '#'

    print(rows, columns, band_members)
    for row in grid:
        print(''.join(row))


generate_bottleneck_input(rows=200, columns=200, band_members=200)
