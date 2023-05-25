from sys import stdin

n = int(next(stdin))

# Multiply bottles by 2 to avoid floating point errors
bottles = list(map(lambda x: int(x) * 2, next(stdin).split()))

# We will query bottles by 2x and 0.5x, so those need to be in the tree
temp_bottles = list(bottles)
temp_bottles.extend(height * 2 for height in bottles)
temp_bottles.extend(height / 2 for height in bottles)

# Reduce bottle heights from 1 ... 10^9 to 1 ... num_heights
bottles_set = set(temp_bottles)
bottle_map = {bottle: i for i, bottle in enumerate(
    sorted(bottles_set), start=1)}

num_heights = len(bottles_set)
max_height = max(bottles_set)


def add(tree, k, amount):
    k = bottle_map[k]
    while k <= num_heights:
        tree[k] += amount
        k += k & -k


def num_smaller_than(tree, k, or_equal_to=True):
    k = bottle_map[k] - (0 if or_equal_to else 1)
    s = 0
    while k >= 1:
        s += tree[k]
        k -= k & -k
    return s


def num_larger_than_or_equal_to(tree, k):
    # The number of bottles with height >= k is the total number of bottles,
    # minus the number of bottles with height < k
    return num_smaller_than(tree, max_height) - num_smaller_than(tree, k, or_equal_to=False)


# Fenwick trees
num_double_on_left = [0] * (num_heights + 1)
potential_triples = [0] * (num_heights + 1)


total_num_triples = 0

for orig_num in bottles:
    num = orig_num
    double = 2 * orig_num
    half = orig_num // 2

    how_many_double_on_left = num_larger_than_or_equal_to(
        num_double_on_left, double)
    num_new_triples = num_larger_than_or_equal_to(potential_triples, num)

    total_num_triples += num_new_triples

    add(num_double_on_left, num, 1)
    add(potential_triples, half, how_many_double_on_left)


print(total_num_triples)
