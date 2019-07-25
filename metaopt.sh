#!/bin/bash

# For figuring out how many processes is best

for i in {1..64}; do
    mpirun -np $i python3 optimizor.py;
done;
