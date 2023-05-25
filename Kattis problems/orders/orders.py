n = int(input())
menu_item_prices = list(map(int, input().split()))

m = int(input())
orders = list(map(int, input().split()))
max_order = max(orders)

# ambiguous[i] = True if there are multiple ways to get to price i
ambiguous = [False] * (max_order + 1)
# possible[i] = True if it is possible to reach price i
possible = [False] * (max_order + 1)
possible[0] = True
# previous[i] = the price of the previous menu item in the path to price i
previous = [None] * (max_order + 1)
previous[0] = 0
# menu_item_number[price] = the index of the menu item with that price
menu_item_number = {}

for i, price in enumerate(menu_item_prices, start=1):
    # Menu items can have the same price
    if price in menu_item_number:
        ambiguous[price] = True
    else:
        menu_item_number[price] = i


# Recreates the path to price i
def recreate_path(i, incl=None):
    path = [] if incl is None else [incl]
    while i > 0:
        path.append(previous[i])
        i -= previous[i]
    return path


# Checks if the new path (from i to i + price) is equal to the existing path to i + price
def are_equal_paths(i, price):
    a = recreate_path(i + price)
    b = recreate_path(i, incl=price)

    if len(a) != len(b):
        return False

    a = sorted(a)
    b = sorted(b)

    for i in range(len(a)):
        if a[i] != b[i]:
            return False

    return True


for i in range(max_order + 1):
    if not possible[i]:
        continue

    for price in menu_item_prices:
        # We don't need to precompute the paths to prices that are too large to be queried
        if i + price > max_order:
            continue

        # If an order is ambiguous, any other reachable order is also ambiguous
        if ambiguous[i]:
            ambiguous[i + price] = True
        # If the order has been reached before, check if the new path is different
        elif possible[i + price] and not ambiguous[i + price]:
            if not are_equal_paths(i, price):
                ambiguous[i + price] = True
        # If the order has not been reached before, add a path to it
        else:
            previous[i + price] = price

        possible[i + price] = True

for order in orders:
    if ambiguous[order]:
        print("Ambiguous")
    elif possible[order]:
        # Map the menu item prices to their menu item numbers
        ans = map(menu_item_number.get, recreate_path(order))
        print(*sorted(ans))
    else:
        print("Impossible")
