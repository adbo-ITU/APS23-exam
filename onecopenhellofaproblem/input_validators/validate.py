#! /usr/env/python3

import sys
import re
import argparse


parser = argparse.ArgumentParser('Input format validator')
parser.add_argument('--min-r', type=int, default=1)
parser.add_argument('--max-r', type=int, default=500)
parser.add_argument('--min-c', type=int, default=1)
parser.add_argument('--max-c', type=int, default=500)
parser.add_argument('--min-b', type=int, default=1)
parser.add_argument('--max-b', type=int, default=500)
args = parser.parse_args()


line = sys.stdin.readline()

assert re.match(r"[1-9][0-9]* [1-9][0-9]* [1-9][0-9]*\n", line), line

r, c, b = map(int, line.split())

assert args.min_r <= r <= args.max_r, f'r = {r}'
assert args.min_c <= c <= args.max_c, f'c = {c}'
assert args.min_b <= b <= args.max_b, f'b = {b}'

for i in range(r):
    line = sys.stdin.readline()
    assert re.match(r"^([#\.]+)\n", line), f'Line {i}'
    assert len(line.strip()) == c, f'Line {i}'

assert sys.stdin.readline() == ""

sys.exit(42)
