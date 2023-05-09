n = int(input())

input = list(map(lambda x: int(x)*2, input().split()))
bottles = list(input)
bottles.extend([height*2 for height in input])
bottles.extend([height/2 for height in input])

bottleset = sorted(set(bottles))
num_heights = len(bottleset)

bottlemap = dict([(bottle, i) for i, bottle in enumerate(bottleset,1)])

trios = [0]*(n)
l = [0]*(n)
r = [0]*(n)

max_height = max(bottleset)
tree_len = num_heights

left_tree = [0]*(num_heights+1)
right_tree = [0]*(num_heights+1)

def add(tree, k):
    k = bottlemap[k]
    while k <= tree_len:
        tree[k] += 1
        k += k&-k 

def numSmallerThanOrEqual(tree, k, stop_early=False):
    # print(k, end=' ')
    k = bottlemap[k]
    # print('turned into', k)
    s = 0

    if stop_early:
        k -= 1
    while k>=1: 
        s += tree[k]
        k -= k&-k
    return s

def numSmallerThan(tree, k):
    return numSmallerThanOrEqual(tree, k, stop_early=True)

# TODO: replace this with a true range sum method
def range(tree, k):
    # print(range_sum(tree, max_height), '-', range_sum(tree, min(max_height, k)))
    return range_sum(tree, max_height) - range_sum(tree, min(max_height, k))

def numLargerThanOrEqual(tree, k):
    total = numSmallerThanOrEqual(tree, max_height)
    smaller_or_equal = numSmallerThan(tree, k)
    #print(total, smaller_or_equal)
    #print("Number of heights at least", k, "is", total - smaller_or_equal)
    return total - smaller_or_equal
    '''
    k = bottlemap[k]
    s = 0
    while k <= num_heights:
        s += tree[k]
        k += k&-k
    return s
    '''
# Sweeping left-to-right
for i, bottle in enumerate(input):
    #l[i] = range(left_tree, bottle*2-1)
    #trios[i] = range(left_tree, bottle*2-1)
    trios[i] = numLargerThanOrEqual(left_tree, bottle*2)
    add(left_tree, bottle)

# Sweeping right-to-left
for i, bottle in reversed(list(enumerate(input))):
    trios[i] *= numSmallerThanOrEqual(right_tree, bottle/2)
    #r[i] = numSmallerThanOrEqual(right_tree, bottle/2)
    add(right_tree, bottle)

print(sum(trios))





            
