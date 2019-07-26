# Distributable distribution solver

This program solves a flavour of the Vehicle Routing Problem. Not an elegant solution by any means, but it does support `mpi`, so if you wanna max out 16 computers' CPU's at once trying to solve an arbitrary transportation problem, look no further.

## Problem

You have x delivery vehicles, y different pickup locations, y different drop-off locations and a map of size a * b. Find the most efficient set of instructions to do all deliveries. I.e. smallest distance travelable to make all deliveries. 

## Strat

The program finds the best solution by running multiple pseudo-random simulations and taking the solution with the lowest cost. Multiple optimisation strategies makes this algorithm (ironically enough) a serious contender in a competitive programming environment.

## Optimisations

- Search space splitting: Split the search space equally among processes. Parallelisation really decreases runtime drastically. 
- Once a simulation's running cost exceeds already-known best cost, the solver stops and moves to the next iteration.
- (Optional) Distribution control: For each distribution type (how tasks are distributed among delivery vehicles) run the entire search space. This drastically increases work done per search space unit, but theoretically you should get better answers in relatively smaller search spaces. 

## Running

To run, use mpirun. Eg:

    mpirun -np 8 python3 main.py
    
mpirun supports many flags. `-np 8` specifies that 8 processes should be used. You can specify multiple nodes (computers) too. Check out an mpi tutorial for details.

## Config

When the program is run, the config file, `config.yml` is read to determine how to run the program. Here's how things work: 

Key | Description | Example
--- | --- | ---
`SEARCH_SPACE` | The amount of seeds to check. Will be evaluated by python at runtime | `2 ** 16`
`UPDATES_PER_RANK` | Amount of progress updates you want to see for each process. Typically you want this number big if you think it will take long to run.| `20`
`VERBOSE` | Will print progress only if true. | `true`
`CONTROL_DISTRIBUTIONS` | Opt to run the program with controlled distributions enabled. (See above)| `false` 
`MAPNO` | Map number. Map input files should be named: map_**x**.input. See example maps for format. | `3`
`WRITE_SOLUTION` | After best solution has been found, write it to a file. It will be in the same dir as the input file, named: map_**x**.output. | `true`
`INDEFINITE` | Keep running indefinitely, printing new best results as they're found. Theoretically, at some point the program will start doing duplicate work. This will happen even faster with more threads, so don't just leave this running overnight without thinking. `SEARCH_SPACE` and `CONTROL_DISTRIBUTIONS` will be ignored. | `false`
`SHUFFLE_MODE` | Shuffle tasks before assigning them randomly. Some other options will be ignored. | `true` 

## Todo's

*Don't count on these ever happening. If you're bored, make a PR.*

- Replace file locking with something in-memory. 
- Store final result with searchspace, so next run program continues to next space-step
- Set up distribution centre for better managing of distribution kinds.
