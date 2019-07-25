import problem
import runner
from mpi4py import MPI
import sys
import time
import yaml

# config
cfg = yaml.safe_load(open('config.yml'))
VERBOSE = cfg['VERBOSE']
UPDATES_PER_RANK = cfg['UPDATES_PER_RANK']
MAPNO = cfg['MAPNO']
SEARCH_SPACE = eval(cfg['SEARCH_SPACE'])
CONTROL_DISTRIBUTIONS = cfg['CONTROL_DISTRIBUTIONS']
WRITE_SOLUTION = cfg['WRITE_SOLUTION']

# static vars
comm = MPI.COMM_WORLD
current_rank = comm.rank
total_ranks = comm.size


def run_subset(prob: problem.Problem, start, gap, rankid):
    best_seed = start
    best_res = _run_solve(prob, best_seed)

    # run the subset
    for i in range(start + 1, start + gap + 1):
        res = _run_solve(prob, i, max_cost=best_res)
        if res < best_res:
            best_res = res
            best_seed = i

        if VERBOSE and (i - start - 1) % (gap // UPDATES_PER_RANK) == 0:
            print('rank', rankid, 'at', round((i-start-1)*100/gap, 2), '%')
            sys.stdout.flush()

    return [best_res, best_seed]


def run_subset_dc(prob: problem.Problem, start, gap, rankid):
    best_seed = start
    best_distro = runner.gen_distro(prob)
    best_res = _run_solve(prob, best_seed, best_distro)  # to start off with
    distros_ran = {}

    for d in range(gap):
        # setup distro
        distro = runner.gen_distro(prob)
        dstr = runner.dtostr(distro)

        if dstr not in distros_ran:
            # run the subset
            for i in range(start+1, start+gap+1):
                res = _run_solve(prob, i, distro, max_cost=best_res)
                if res < best_res:
                    best_res = res
                    best_seed = i
                    best_distro = distro

            distros_ran[dstr] = True

        # progress update
        if VERBOSE and d % (gap // UPDATES_PER_RANK) == 0:
            print('rank', rankid, 'at', round(d*100/gap, 2), '%')
            sys.stdout.flush()

    return [best_res, best_seed, best_distro]


def _run_solve(prob: problem.Problem, x, distro=None, max_cost=None):
    prob.clear()
    return runner.solve_randomly(prob, int(x), distro, max_cost)


def main():
    start_time = time.time()
    prob = problem.Problem("maps/map_%d.input" % MAPNO)

    search_gap = SEARCH_SPACE//total_ranks
    search_start = search_gap * current_rank

    if current_rank == 0:
        if VERBOSE:
            print('Map', MAPNO, 'loaded. Search space:', SEARCH_SPACE)
            print('-'*8)
        for i in range(1, total_ranks):
            comm.send(True, dest=i, tag=0)  # start signal
    else:
        comm.recv(source=0, tag=0)  # wait for start signal

    if VERBOSE:
        print('running from', search_start, 'to', search_start+search_gap, 'on rank', current_rank)
    sys.stdout.flush()
    this_best = run_subset_dc(prob, search_start, search_gap, current_rank) if CONTROL_DISTRIBUTIONS else \
            run_subset(prob, search_start, search_gap, current_rank)

    if current_rank > 0:
        comm.send(this_best, dest=0, tag=420)
    else:
        # consolidate
        best = this_best
        for i in range(1, total_ranks):
            rec_best = comm.recv(source=i, tag=420)
            if rec_best[0] < best[0]:
                best = rec_best

        if VERBOSE: print('-'*8)
        if CONTROL_DISTRIBUTIONS:
            print('Done. Best score:', best[0], 'seed:', best[1], 'distro:', best[2])
            if WRITE_SOLUTION:
                _run_solve(prob, best[1], best[2])
        else:
            print('Done. Best score:', best[0], 'seed:', best[1])
            if WRITE_SOLUTION:
                _run_solve(prob, best[1])

        if WRITE_SOLUTION:
            prob.write_solution('maps/map_%d.output' % MAPNO)

    return time.time() - start_time  # runtime


