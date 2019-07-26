import simpleprob
import random


def distance(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)


def solve(prob: simpleprob.SimpleProblem, seed: int, max_cost=None):
    random.seed(seed)

    tasks = get_shuffled(prob.tasks)

    total_cost = 0
    for task in tasks:
        randi = random.randint(0, len(prob.delivs)-1)
        total_cost += run_task(prob.delivs[randi], task)

        if max_cost is not None and total_cost >= max_cost:
            break

    return total_cost


def run_task(delivset: list, task: simpleprob.Task) -> int:
    """add task to history and return the cost"""
    this_task_cost = distance(task.sx, task.sy, task.dx, task.dy)

    if len(delivset) == 0:
        delivset.append(task)
        return distance(0, 0, task.sx, task.sy) + this_task_cost
    else:
        last_task = delivset[len(delivset)-1]
        delivset.append(task)
        return distance(last_task.dx, last_task.dy, task.sx, task.sy) + this_task_cost


def get_shuffled(lst: list) -> list:
    """Shuffle by copying"""
    shf = []
    for i in lst:
        shf.append(i)
    random.shuffle(shf)
    return shf