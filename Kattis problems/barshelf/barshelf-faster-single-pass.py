import sys


def main():
    n = int(next(sys.stdin))
    nums = [2 * int(i) for i in next(sys.stdin).split()]

    compressed_nums = {}
    counter = 1
    sorted_nums = sorted(nums + [x * 2 for x in nums] + [x // 2 for x in nums])
    for num in sorted_nums:
        if num not in compressed_nums:
            counter += 1
            compressed_nums[num] = counter

    max_val = counter + 4
    num_double_on_left = FenwickTree(max_val)
    potential_triples = FenwickTree(max_val)
    total_num_triples = 0

    for orig_num in nums:
        num = compressed_nums[orig_num]
        double = compressed_nums[2 * orig_num]
        half = compressed_nums[orig_num // 2]

        how_many_double_on_left = num_double_on_left.range_sum(double, max_val)
        num_new_triples = potential_triples.range_sum(num, max_val)

        total_num_triples += num_new_triples

        num_double_on_left.add(num, 1)
        potential_triples.add(half, how_many_double_on_left)

    print(total_num_triples)


class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def add(self, i, val):
        while i <= len(self.tree):
            self.tree[i] += val
            i += i & (~i + 1)

    def _sum(self, i):
        _sum = 0
        while i > 0:
            _sum += self.tree[i]
            i -= i & (~i + 1)
        return _sum

    def range_sum(self, l, r):
        return self._sum(r) - self._sum(l - 1)


if __name__ == "__main__":
    main()
