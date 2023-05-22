#!/bin/bash
USE_SCORING=1

. ../../_testdata_tools/gen.sh

use_solution maxflow.py

compile generate_input.py

# ---------------
# --- SAMPLES ---
# ---------------
samplegroup
sample_manual 1

# ---------------
# --- GROUP 1 ---
# ---------------
group group1 25
limits --min-r=1 --max-c=1 --max-r=15 --max-c=15
tc 1

for FILE in ../manual-tests/*.in; do
  # tc_manual will use the inputs from the manual-tests directory, but will not
  # use the answer files. Those are just for ourselves when implementing and
  # validating the accepted solution.
  tc_manual $FILE
done

densities=(75 50 25)
for density in "${densities[@]}"; do :
  for i in {1..3}; do :
    tc random_small_density${density}_$i generate_input --approx-density=0.$density --max-r=15 --max-c=15 --max-b 15
  done
done
for i in {1..3}; do :
  tc random_small_bottleneck_$i generate_input --style bottleneck --max-r=15 --max-c=15 --max-b 15
done

# ---------------
# --- GROUP 2 ---
# ---------------
group group2 75
include_group group1
limits --min-r=1 --max-c=1 --max-r=50 --max-c=50
densities=(100 75 50 25)
for density in "${densities[@]}"; do :
  for i in {1..3}; do :
    tc random_large_density${density}_$i generate_input --approx-density=0.$density --min-r 15 --max-r=50 --max-c=50
  done
done
for i in {1..3}; do :
  tc random_large_bottleneck_$i generate_input --style bottleneck --min-r 15 --max-r=50 --max-c=50
done
tc full_size_full_crowd generate_input --approx-density=1 --min-r 50 --min-c 50 --max-r=50 --max-c=50
