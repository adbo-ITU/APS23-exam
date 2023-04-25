# One Copenhell of a Problem

## Development

### Environment

It is strongly recommended to use Kattis' `problemtools` via Docker. Run this in the repository root:

```sh
docker run --rm -it -v $(pwd):/apsdev -w /apsdev hamerly/problemtools-icpc
```

### Verify problem

To verify the validity of the Kattis problem (folders, given accepted/not-accepted solutions, test cases, input format, etc.), run:

```
verifyproblem .
```

The shorthand `(cd data && ./generate.sh) && verifyproblem .` may come in useful to just generate test cases and verify the problem in one go.

### Generating test data

For test data generation, we have used [Kodsport's `testdata_tools`](https://github.com/Kodsport/testdata_tools).

Generate test data automatically by the `generate.sh` script:

```sh
cd data && ./generate.sh
```

### Problem statement

To generate the problem description (including sample cases), run either `problem2pdf .` or `problem2html .`.
