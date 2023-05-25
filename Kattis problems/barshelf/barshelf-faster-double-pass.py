import sys


def main():
    n = int(next(sys.stdin))
    nums = [2 * int(i) for i in next(sys.stdin).split()]

    sorted_nums = sorted(nums + [x * 2 for x in nums] + [x // 2 for x in nums])

    compressed_nums = {}
    counter = 1
    for num in sorted_nums:
        if num not in compressed_nums:
            counter += 1
            compressed_nums[num] = counter

    max_val = counter + 4
    left_tree = FenwickTree(max_val)
    right_tree = FenwickTree(max_val)

    trios = [0] * n
    enumerated_bottles = list(enumerate(nums))

    # Sweeping left-to-right
    for i, bottle in enumerated_bottles:
        num = compressed_nums[bottle]
        double = compressed_nums[2 * bottle]

        trios[i] = left_tree.range_sum(double, max_val)
        left_tree.add(num, 1)

    # Sweeping right-to-left
    total = 0
    for i, bottle in reversed(enumerated_bottles):
        num = compressed_nums[bottle]
        half = compressed_nums[bottle // 2]

        total += trios[i] * right_tree.range_sum(1, half)
        right_tree.add(num, 1)

    print(total)


class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def add(self, i, val):
        while i <= len(self.tree):
            self.tree[i] += val
            i += i & (~i + 1)

    def sum(self, i):
        _sum = 0
        while i > 0:
            _sum += self.tree[i]
            i -= i & (~i + 1)
        return _sum

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)


if __name__ == "__main__":
    main()
