use std::{
    collections::HashMap,
    io::{stdin, stdout, BufWriter, Read, Write},
};

fn main() {
    let mut stdin = stdin().lock();
    let mut input_str = String::new();
    stdin.read_to_string(&mut input_str).unwrap();
    let mut stdout = BufWriter::new(stdout().lock());

    let mut input = input_str.split_whitespace();

    let n = read_num(&mut input);
    // double all numbers so we cal safely divide by two and get an integer
    let nums = (0..n).map(|_| 2 * read_num(&mut input)).collect::<Vec<_>>();

    // Perform index compression, i.e. compress all numbers to a consecutive
    // range of integers that we can use as indices in the Fenwick tree. We
    // maintain order!
    let mut compressed_nums = HashMap::new();
    let mut counter = 1;
    let mut sorted = nums.clone();
    sorted.extend(nums.iter().map(|x| x * 2)); // also make space for all doubled numbers
    sorted.extend(nums.iter().map(|x| x / 2)); // also make space for all halved numbers
    sorted.sort_unstable();
    for num in sorted {
        compressed_nums.entry(num).or_insert_with(|| {
            counter += 1;
            counter
        });
    }
    let max = counter;

    // Go through all numbers, for each number keeping track of how many at-
    // least-double-the-size numbers we have seen on the left.
    let mut num_double_on_left = FenwickTree::new(counter + 4);
    let mut potential_triples = FenwickTree::new(counter + 4);
    let mut total_num_triples = 0;

    for orig_num in nums {
        let num = *compressed_nums.get(&orig_num).unwrap();
        let double = *compressed_nums.get(&(2 * orig_num)).unwrap();
        let half = *compressed_nums.get(&(orig_num / 2)).unwrap();

        let how_many_double_on_left = num_double_on_left.range_sum(double, max);
        let num_new_triples = potential_triples.range_sum(num, max);

        total_num_triples += num_new_triples;

        num_double_on_left.add(num, 1);
        potential_triples.add(half, how_many_double_on_left);
    }

    writeln!(stdout, "{total_num_triples}").unwrap();
}

/// Everything is 1-indexed!
struct FenwickTree {
    tree: Vec<i64>,
}

impl FenwickTree {
    fn new(n: usize) -> Self {
        Self {
            tree: vec![0; n + 1],
        }
    }

    fn add(&mut self, mut i: usize, val: i64) {
        while i <= self.tree.len() {
            self.tree[i] += val;
            i += i & (!i + 1);
        }
    }

    fn sum(&self, mut i: usize) -> i64 {
        let mut sum = 0;
        while i > 0 {
            sum += self.tree[i];
            i -= i & (!i + 1);
        }
        sum
    }

    fn range_sum(&self, l: usize, r: usize) -> i64 {
        self.sum(r) - self.sum(l - 1)
    }
}

#[inline(always)]
fn read_num<'a>(input: &mut impl Iterator<Item = &'a str>) -> usize {
    input.next().unwrap().parse().unwrap()
}
