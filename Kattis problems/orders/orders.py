from random import randint

n = int(input())
menu_item_prices = list(map(int, input().split()))

m = int(input())
orders = list(map(int, input().split()))
max_order = max(orders) + 1

# alt_price_sum[i] = the sum of the 'alternative' prices of the menu items in the path to price i
alt_price = {menu_item: randint(10 ** 8, 10 ** 9) for menu_item in menu_item_prices}
alt_price_sum = [0] * max_order
# ambiguous[i] = True if there are multiple ways to get to price i
ambiguous = [False] * max_order
# previous[i] = the price of the previous menu item in the path to price i
previous = [None] * max_order
previous[0] = 0

menu_item_number = {}
for i, price in enumerate(menu_item_prices, start=1):
    # Menu items with the same price are ambiguous
    if price in menu_item_number:
        ambiguous[price] = True

    menu_item_number[price] = i

# Precompute the paths to all reachable prices
for i in range(max_order):
    if previous[i] is None:
        continue

    for price in menu_item_prices:
        # We don't need to precompute the paths to prices that are too large to be queried
        if i + price >= max_order:
            continue

        # If an order is ambiguous, any other reachable order is also ambiguous
        if ambiguous[i]:
            ambiguous[i + price] = True
        # If the order has been reached before, check if the new path is different
        elif previous[i + price] is not None and alt_price_sum[i + price] != alt_price_sum[i] + alt_price[price]:
            ambiguous[i + price] = True

        # Add the menu item to the sum of the 'alternative' prices
        alt_price_sum[i + price] = alt_price_sum[i] + alt_price[price]
        # Add the menu item to the path
        previous[i + price] = price

for order in orders:
    if ambiguous[order]:
        print("Ambiguous")
    elif previous[order] is not None:
        path = []
        while order > 0:
            path.append(menu_item_number[previous[order]])
            order -= previous[order]
        print(*sorted(path))
    else:
        print("Impossible")
