# Generic vehicle routing problem


def distance(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)


class Deliv:
    x,y = 0,0
    moves = None
    cost = 0
    moves_avail = 0

    def __init__(self):
        self.moves = list()

    def make_move(self, src, dest):
        """move from current pos to source to dest and do delivery"""
        self.moves.append(src.label)
        move_cost = distance(self.x, self.y, src.x, src.y)
        self.x, self.y = src.x, src.y
        src.hasstuff = False

        self.moves.append(dest.label)
        move_cost += distance(self.x, self.y, dest.x, dest.y)
        self.x, self.y = dest.x, dest.y
        dest.delivered = True

        self.moves_avail -= 1

        self.cost += move_cost
        return move_cost

    def clear(self):
        self.x, self.y = 0, 0
        self.cost = 0
        self.moves = list()
        self.moves_avail = 0


class Source:
    x,y = 0,0
    hasstuff = True
    label = ''

    def __init__(self, x, y, label):
        self.x, self.y = x, y
        self.label = label


class Dest:
    x, y = 0, 0
    delivered = False
    label = ''

    def __init__(self, x, y, label):
        self.x, self.y = x, y
        self.label = label


class Problem:
    delivs = list()
    sources = list()
    dests = list()
    map = list()

    def __init__(self, infile):
        f = open(infile, 'r')
        splat = f.readline().split(',')

        for i in range(int(splat[0])):
            self.delivs.append(Deliv())

        map_w, map_h = int(splat[3]), int(splat[4])

        for y in range(map_h-1, -1, -1):
            line = f.readline()
            mapline = []
            for x in range(map_w):
                c = line[x]
                if c != '#':
                    if c.isupper():
                        self.sources.append(Source(x, y, c))
                    else:
                        self.dests.append(Dest(x, y, c))
                mapline.append(c)
            self.map.append(mapline)

        f.close()

    def is_solved(self) -> bool:
        for dest in self.dests:
            if not dest.delivered:
                return False
        return True

    def sources_todo(self) -> [Source]:
        todo = []
        for src in self.sources:
            if src.hasstuff:
                todo.append(src)
        return todo

    def delivs_avail(self) -> [Deliv]:
        delavail = []
        for deliv in self.delivs:
            if deliv.moves_avail > 0:
                delavail.append(deliv)
        return delavail

    def get_place(self, c):
        if c.isupper():
            for src in self.sources:
                if src.label == c:
                    return src
        else:
            for dest in self.dests:
                if dest.label == c:
                    return dest
        return None

    def total_cost(self):
        cost = 0
        for deliv in self.delivs:
            cost += deliv.cost
        return cost

    def write_solution(self, outfile):
        f = open(outfile, 'w')
        for deliv in self.delivs:
            if deliv.cost > 0:
                print(','.join(deliv.moves), file=f)
        f.close()

    def clear(self):
        for deliv in self.delivs:
            deliv.clear()
        for src in self.sources:
            src.hasstuff = True
        for dest in self.dests:
            dest.delivered = False

    def apply_distro(self, distro: []):
        for i in range(len(distro)):
            self.delivs[i].moves_avail = distro[i]

