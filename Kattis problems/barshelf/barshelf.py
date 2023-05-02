n = int(input())

input = list(map(lambda x: int(x)*2, input().split()))
bottles = list(input)
bottles.extend([height*2 for height in input])
bottles.extend([height/2 for height in input])

bottleset = sorted(set(input))
num_heights = len(bottleset)

bottlemap = dict([(bottle, i) for i, bottle in enumerate(bottleset,1)])

# add all (bottle*2)*2 and (bottle*2)/2

trios = [0]*(n)
l = [0]*(n)
r = [0]*(n)

max_height = max(bottleset)
tree_len = num_heights

left_tree = [0]*(num_heights*3+1)
right_tree = [0]*(num_heights*3+1)

def add(tree, k):
    k = bottlemap[k]
    while k <= tree_len:
        tree[k] += 1
        k += k&-k 

def range_sum(tree, k):
    # print(k, end=' ')
    k = bottlemap[k]
    # print('turned into', k)
    s = 0
    while k>=1: 
        s += tree[k]
        k -= k&-k
    return s

# TODO: replace this with a true range sum method
def range(tree, k):
    # print(range_sum(tree, max_height), '-', range_sum(tree, min(max_height, k)))
    return range_sum(tree, max_height) - range_sum(tree, min(max_height, k))

# Sweeping left-to-right
for i, bottle in enumerate(bottles):
    l[i] = range(left_tree, bottle*2-1)
    trios[i] = range(left_tree, bottle*2-1)
    add(left_tree, bottle)

# Sweeping right-to-left
for i, bottle in reversed(list(enumerate(bottles))):
    trios[i] *= range_sum(right_tree, bottle/2)
    r[i] = range_sum(right_tree, bottle/2)
    add(right_tree, bottle)

print(sum(trios))





            
