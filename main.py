import meta_random
import meta_random_indef
import meta_shuffle_indef
import yaml
from mpi4py import MPI

cfg = yaml.safe_load(open('config.yml'))

# static vars
comm = MPI.COMM_WORLD
current_rank = comm.rank
total_ranks = comm.size


if __name__ == '__main__':
    if cfg['SHUFFLE_MODE']:
        meta_shuffle_indef.main()
    elif cfg['INDEFINITE']:
        meta_random_indef.main()
    else:
        t = meta_random.main()
        if current_rank == 0:
            print('runtime:', round(t, 2), 's, with', total_ranks, 'processes')

