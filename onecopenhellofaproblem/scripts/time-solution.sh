#!/bin/bash

# Usage: ./scripts/time-solution.sh

set -e

seeds=(12 123 1234 1337 420 666 321 543 3411 4093)
dims=(100 75 50 25 10)
densities=(1 0.75 0.5 0.25 0.1)

mkdir -p bench-out

echo "Running benchmarks..."
echo -e "r \t c \t b \t d \t time \t seed"
echo -e "--- \t --- \t --- \t --- \t ---- \t ----"


# usage: avg_time n command ...
avg_time() {
    n=$1; shift
    (($# > 0)) || return                   # bail if no command given
    for ((i = 0; i < n; i++)); do
        { time -p "$@" &>/dev/null; } 2>&1 # ignore the output of the command
                                           # but collect time's output in stdout
    done | awk '
        /real/ { real = real + $2; nr++ }
        /user/ { user = user + $2; nu++ }
        /sys/  { sys  = sys  + $2; ns++}
        END    {
                 printf("%.1f\n", real/nr);
               }'
}

for seed in "${seeds[@]}"
do : 
  middlemanfile=bench-out/$seed.txt

  for dim in "${dims[@]}"
  do : 
    r=$dim
    c=$dim
    b=1

    for density in "${densities[@]}"
    do : 
        python3 ./data/generate_input.py \
          --style random \
          --min-r $r \
          --max-r $r \
          --min-c $c \
          --max-c $c \
          --min-b $b \
          --approx-density $density \
          $seed \
          > $middlemanfile

      avg=$(avg_time 1 \
        pypy3 submissions/accepted/maxflow.py < $middlemanfile)

      echo -e "$r \t $c \t $b \t $density \t ${avg}s \t $seed"
    done
  done

  echo -ne "\n"
done
