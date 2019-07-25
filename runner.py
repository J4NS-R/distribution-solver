import random
import problem


def gen_distro(prob: problem.Problem) -> [int]:
    """generate a random distro set for the number of delivs and tasks"""
    delivs = len(prob.delivs)
    tasks = len(prob.sources)
    ou = [0 for i in range(delivs)]
    i = 0
    while tasks > 0:
        delta = random.randint(1, tasks)
        ou[i] += delta
        tasks -= delta
        i = (i + 1) % delivs
    return ou


def dtostr(distro: []) -> str:
    """convert a distro set to a hashable str"""
    storable = ''
    for d in sorted(distro):
        if d != 0:
            storable += str(d) + ','
    return storable


def solve_randomly(prob: problem.Problem, seed: int, distro: [] = None, max_cost=None):
    random.seed(seed)

    if distro is None:
        prob.apply_distro(gen_distro(prob))
    else:
        prob.apply_distro(distro)

    cost_so_far = 0
    while not prob.is_solved():
        todo = prob.sources_todo()
        delivs = prob.delivs_avail()
        random.shuffle(todo)

        if len(todo) < len(delivs):
            i = 0
            for t in todo:
                cost_so_far += delivs[i].make_move(t, prob.get_place(t.label.lower()))
                i += 1
        else:
            i = 0
            for deliv in delivs:
                cost_so_far += deliv.make_move(todo[i], prob.get_place(todo[i].label.lower()))
                i += 1

        if max_cost is not None and cost_so_far >= max_cost:
            break  # stop execution if this seed is infeasible.

    return cost_so_far


if __name__ == '__main__':
    prob = problem.Problem("maps/map_3.input")
    res = solve_randomly(prob, 2357970)
    print(res)
    prob.write_solution("maps/map_3_score_%d.output" % res)


