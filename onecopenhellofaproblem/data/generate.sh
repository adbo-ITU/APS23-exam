#!/bin/bash
USE_SCORING=1

. ../../_testdata_tools/gen.sh

use_solution greedy.py

compile generate_input.py

# ---------------
# --- SAMPLES ---
# ---------------
samplegroup
sample_manual 1

# ---------------
# --- GROUP 1 ---
# ---------------
group group1 75
limits --min-r=1 --min-c=1 --max-r=75 --max-c=75

tc 1

for FILE in ../manual-tests/*.in; do
  # tc_manual will use the inputs from the manual-tests directory, but will not
  # use the answer files. Those are just for ourselves when implementing and
  # validating the accepted solution.
  tc_manual $FILE
done

densities=(100 75 50 25)
for density in "${densities[@]}"; do :
  for i in {1..3}; do :
    tc random_small_density${density}_$i generate_input --approx-density=0.$density --min-r=1 --min-c=1 --max-r=75 --max-c=75
  done
done
for i in {1..3}; do :
  tc random_small_bottleneck_$i generate_input --style bottleneck --min-r=1 --min-c=1 --max-r=75 --max-c=75
done
tc full_size_small_full_crowd generate_input --approx-density=1 --min-r 75 --min-c 75 --max-r=75 --max-c=75 --min-b 75 --max-b 75

# ---------------
# --- GROUP 2 ---
# ---------------
group group2 25
include_group group1
limits --min-r=1 --min-c=1 --max-r=500 --max-c=500

densities=(100 75 50 25)
for density in "${densities[@]}"; do :
  for i in {1..3}; do :
    tc random_large_density${density}_$i generate_input --approx-density=0.$density --min-r 75
  done
done
for i in {1..3}; do :
  tc random_large_bottleneck_$i generate_input --style bottleneck --min-r 75
done
tc full_size_large_full_crowd generate_input --approx-density=1 --min-r 500 --min-c 500 --max-r=500 --max-c=500 --min-b 500 --max-b 500
