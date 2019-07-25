import sys
import time
import fcntl
import problem
import runner
from mpi4py import MPI
import yaml

# config
cfg = yaml.safe_load(open('config.yml'))
VERBOSE = cfg['VERBOSE']
MAPNO = cfg['MAPNO']
WRITE_SOLUTION = cfg['WRITE_SOLUTION']

# static vars
comm = MPI.COMM_WORLD
current_rank = comm.rank
total_ranks = comm.size


def _wait_lock(f):  # this doesn't work when you have like 30 threads trying to lock at the same time.
    while True:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except (OSError, IOError) as e:
            pass
        time.sleep(0.1)


def read_global_best() -> int:
    f = open('.best', 'r')

    _wait_lock(f)
    bst = f.readline()

    fcntl.flock(f, fcntl.LOCK_UN)
    f.close()
    return int(bst)


def write_global_best(new_best: int, seed: int):
    f = open('.best', 'w')
    _wait_lock(f)  # gotta lock files to make threads play nice together
    print(new_best, file=f)
    print('seed:', seed, file=f)
    f.flush()
    fcntl.flock(f, fcntl.LOCK_UN)
    f.close()

    print('New best found:', new_best, 'seed:', seed)
    sys.stdout.flush()


def main():
    prob = problem.Problem("maps/map_%d.input" % MAPNO)

    best_cost = runner.solve_randomly(prob, 0)  # to start with

    if current_rank == 0:
        # write initial value and send start signal
        write_global_best(best_cost, 0)
        for i in range(1, total_ranks):
            comm.send(True, dest=i, tag=0)
    else:
        # wait for start signal
        comm.recv(source=0, tag=0)

    x = int(time.time() * current_rank)
    danger_zone = int(time.time() * (current_rank + 1))

    while True:
        prob.clear()
        cost = runner.solve_randomly(prob, x, max_cost=best_cost)

        if cost < best_cost:  # should be a rarity
            global_best = read_global_best()
            if cost < global_best:
                write_global_best(cost, x)
                best_cost = cost

                if WRITE_SOLUTION:
                    prob.write_solution('maps/map_%d.output' % MAPNO)

            else:
                best_cost = global_best

        x += 1
        if x >= danger_zone:
            print('Breaking thread', current_rank, '. Search space exhausted!')
            break



