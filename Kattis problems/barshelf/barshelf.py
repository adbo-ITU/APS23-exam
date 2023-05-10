n = int(input())

# Multiply bottles by 2 to avoid floating point errors
bottles = list(map(lambda x: int(x) * 2, input().split()))

# We will query bottles by 2x and 0.5x, so those need to be in the tree
temp_bottles = list(bottles)
temp_bottles.extend(height * 2 for height in bottles)
temp_bottles.extend(height / 2 for height in bottles)

# Reduce bottle heights from 1 ... 10^9 to 1 ... num_heights
bottles_set = set(temp_bottles)
bottle_map = {bottle: i for i, bottle in enumerate(sorted(bottles_set), start=1)}

num_heights = len(bottles_set)
max_height = max(bottles_set)


def add(tree, k):
    k = bottle_map[k]
    while k <= num_heights:
        tree[k] += 1
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
    # minus the number of bottles with height <= k
    return num_smaller_than(tree, max_height) - num_smaller_than(tree, k, or_equal_to=False)


# Fenwick trees
left_tree = [0] * (num_heights + 1)
right_tree = [0] * (num_heights + 1)

# Number of trios for each bottle
trios = [0] * n
enumerated_bottles = list(enumerate(bottles))

# Sweeping left-to-right
for i, bottle in enumerated_bottles:
    trios[i] = num_larger_than_or_equal_to(left_tree, bottle * 2)
    add(left_tree, bottle)

# Sweeping right-to-left
for i, bottle in reversed(enumerated_bottles):
    trios[i] *= num_smaller_than(right_tree, bottle / 2)
    add(right_tree, bottle)

print(sum(trios))
