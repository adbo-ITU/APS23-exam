#!/bin/bash
USE_SCORING=1

. ../../_testdata_tools/gen.sh

use_solution maxflow.py

compile generate_random_bottleneck.py

samplegroup
sample_manual 1

group group1 50
tc 1
for FILE in ./manual-tests/*.in; do
  # tc_manual will use the inputs from the manual-tests directory, but will not
  # use the answer files. Those are just for ourselves when implementing and
  # validating the accepted solution.
  tc_manual $FILE
done
