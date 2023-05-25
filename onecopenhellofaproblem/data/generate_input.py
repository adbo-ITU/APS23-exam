#!/usr/bin/python3

import random
import argparse
import sys


parser = argparse.ArgumentParser('Random input generator')
# By convention, the last argv argument is a random seed. So we just have a positional argument for this.
parser.add_argument('seed', type=int)
parser.add_argument('--min-r', type=int, default=1)
parser.add_argument('--max-r', type=int, default=500)
parser.add_argument('--min-c', type=int, default=1)
parser.add_argument('--max-c', type=int, default=500)
parser.add_argument('--min-b', type=int, default=1)
parser.add_argument('--max-b', type=int, default=500)
parser.add_argument('--style', type=str, default="random",
                    choices=["random", "bottleneck"])


# From https://stackoverflow.com/questions/55324449/how-to-specify-a-minimum-or-maximum-float-value-with-argparse
def range_limited_float_type(arg):
    """ Type function for argparse - a float within some predefined bounds """
    MIN_VAL = 0.0
    MAX_VAL = 1.0
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f < MIN_VAL or f > MAX_VAL:
        raise argparse.ArgumentTypeError(
            f"Argument must be in range [{MIN_VAL}; {MAX_VAL}]")
    return f


parser.add_argument('--approx-density',
                    type=range_limited_float_type, default=0.75)

args = parser.parse_args()

random.seed(args.seed)

r = random.randint(args.min_r, args.max_r)
c = random.randint(args.min_c, args.max_c)
b = random.randint(args.min_b, args.max_b)


def generate_random(rows, columns, band_members, density=args.approx_density):
    grid = [['.' for _ in range(columns)] for _ in range(rows)]
    count = 0
    for row in grid:
        for j in range(len(row)):
            if random.uniform(0, 1) <= density:
                row[j] = '#'
                count += 1

    print(rows, columns, band_members)
    for row in grid:
        print(''.join(row))


# Mostly useful for catching if the solution respects the node-disjoint constraint.
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
        step_size = 4 if i == len(grid) // 2 else 2
        for j in range(0, len(row) - 1, step_size):
            row[j + random.randint(0, 1)] = '#'

    print(rows, columns, band_members)
    for row in grid:
        print(''.join(row))


kw_args = {"rows": r, "columns": c, "band_members": b}

if args.style == "random":
    generate_random(**kw_args)
elif args.style == "bottleneck":
    generate_bottleneck_input(**kw_args)
