class Task:

    def __init__(self):
        self.src, self.sx, self.sy, self.dest, self.dx, self.dy = tuple([None] * 6)

    def set_src(self, label, x, y):
        self.src = label
        self.sx = x
        self.sy = y

    def set_dest(self, label, x, y):
        self.dest = label
        self.dx = x
        self.dy = y


class SimpleProblem:

    def _get_task(self, label) -> Task:
        for t in self.tasks:
            if t.src == label or t.dest == label or t.src == label.upper() or t.dest == label.lower():
                return t

        t = Task()
        self.tasks.append(t)
        return t

    def __init__(self, infile: str):
        self.tasks = []

        f = open(infile, 'r')
        splat = f.readline().split(',')

        self.deliv_count = int(splat[0])
        self.delivs = []
        for i in range(self.deliv_count):
            self.delivs.append(list())

        map_w, map_h = int(splat[3]), int(splat[4])

        for y in range(map_h - 1, -1, -1):
            line = f.readline()
            for x in range(map_w):
                c = line[x]
                if c != '#':
                    if c.isupper():
                        self._get_task(c).set_src(c, x, y)
                    else:
                        self._get_task(c).set_dest(c, x, y)

        f.close()

    def write_solution(self, outfile):
        f = open(outfile, 'w')
        for deliv in self.delivs:
            if len(deliv) > 0:
                line = ''
                for t in deliv:
                    line += t.src + ',' + t.dest + ','
                print(line[:-1], file=f)
        f.close()

    def clear(self):
        self.delivs = []
        for i in range(self.deliv_count):
            self.delivs.append(list())
