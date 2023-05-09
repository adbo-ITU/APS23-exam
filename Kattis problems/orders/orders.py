n = int(input())
menu_items = list(map(int, input().split()))

m = int(input())
orders = list(map(int, input().split()))

max_order = max(orders)
ambiguous = [False] * (max_order + 1)
possible = [False] * (max_order + 1)
possible[0] = True

path = []
for i in range(max_order + 1):
    path.append([])

menu_item_number = dict((item, i) for i, item in enumerate(menu_items, start=1))

def are_equal_paths(a, b):
    if len(a) != len(b):
        return False

    a = sorted(a)
    b = sorted(b)
    for i in range(len(a)):
        if a[i] != b[i]:
            False

    return True

for i in range(max_order + 1):
    if not possible[i]:
        continue

    for item in menu_items:
        if i + item > max_order:
            continue

        if ambiguous[i]:
            ambiguous[i + item] = True
        elif possible[i + item] and not ambiguous[i + item]:
            if not are_equal_paths(path[i] + [item], path[i + item]):
                ambiguous[i + item] = True
        else:
            path[i + item] = path[i] + [item]

        possible[i + item] = True

# for i in range(max_order + 1):
#     print(i, "Ambiguous:", ambiguous[i], "Possible:", possible[i], "Path:", path[i])

for order in orders:
    if ambiguous[order]:
        print("Ambiguous")
    elif possible[order]:
        ans = map(menu_item_number.get, path[order])
        print(*sorted(ans))
    else:
        print("Impossible")
