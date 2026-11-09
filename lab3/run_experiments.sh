#!/bin/bash
SIZES="200 400 800 1200 1600 2000"
PROCS="1 2 4 8"

mkdir -p input output
> results.txt
echo "N Procs Time_s" >> results.txt

for N in $SIZES; do
    echo "Generating N=$N..."
    python3 -c "
import random
n = $N
with open('input/A_$N.txt', 'w') as f:
    f.write(str(n) + '\n')
    for _ in range(n):
        f.write(' '.join(str(random.uniform(-10, 10)) for _ in range(n)) + '\n')
with open('input/B_$N.txt', 'w') as f:
    f.write(str(n) + '\n')
    for _ in range(n):
        f.write(' '.join(str(random.uniform(-10, 10)) for _ in range(n)) + '\n')
" 2>/dev/null || echo "Python not found"

    for P in $PROCS; do
        if [ ! -f "input/A_$N.txt" ]; then continue; fi
        echo "Running N=$N, Procs=$P..."
        OUTPUT=$(mpirun -np $P ./lab3_mpi input/A_$N.txt input/B_$N.txt output/C_$N.txt 2>&1)
        TIME=$(echo "$OUTPUT" | grep "time =" | awk '{print $3}')
        
        if [ -n "$TIME" ]; then
            echo "$N $P $TIME" >> results.txt
            echo "  -> Time: $TIME s"
        else
            echo "$N $P FAIL" >> results.txt
            echo "  -> Failed"
        fi
    done
done
echo "Done!"