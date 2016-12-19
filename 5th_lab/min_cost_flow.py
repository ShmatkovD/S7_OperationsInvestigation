# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class Web(object):

    def __init__(self, a, c):
        self._c = c
        self._n = len(a)

    def count_potentials(self, b):
        u = [0] * self._n
        for i, j in b:
            u[i] = None
            u[j] = None

        u[0] = 0
        while any(i is None for i in u):
            for i, j in b:
                if u[i] is None and u[j] is not None:
                    u[i] = u[j] + self._c[i, j]
                elif u[i] is not None and u[j] is None:
                    u[j] = u[i] - self._c[i, j]
        return u

    def find_cycle(self, b, frm, to):
        g = [[] for _ in range(self._n)]
        for i, j in b.keys():
            g[i].append(j)
            g[j].append(i)

        queue = [frm]
        used = [False] * self._n
        prev = [-1] * self._n
        while queue:
            i = queue.pop(0)
            used[i] = True
            for j in g[i]:
                if not used[j]:
                    prev[j] = i
                    queue.append(j)

        cycle = []
        i = to
        while prev[i] != -1:
            cycle.append((prev[i], i))
            i = prev[i]
        return cycle

    def min_cost_flow(self, b):
        while True:
            u = self.count_potentials(b)
            delta = {}
            for i, j in self._c:
                if not (i, j) in b:
                    delta[i, j] = u[i] - u[j] - self._c[i, j]

            if all(d <= 0 for d in delta.values()):
                return b

            i0, j0 = filter(lambda (i, j): delta[i, j] > 0, delta)[0]
            cycle = self.find_cycle(b, j0, i0)

            theta, ix, jx = float('inf'), 0, 0
            for j, i in cycle:
                if (i, j) in b:
                    if theta > b[i, j]:
                        theta, ix, jx = b[i, j], i, j

            for i, j in cycle:
                if (i, j) in b:
                    b[i, j] += theta
                if (j, i) in b:
                    b[j, i] -= theta

            del b[ix, jx]
            b[i0, j0] = theta


def main():
    cases = [
        dict(
            a=[
                1, -4, -5, -6, 5, 9,
            ],
            c={
                (0, 1): 1,
                (1, 5): 3,
                (2, 1): 3,
                (2, 3): 5,
                (4, 2): 4,
                (4, 3): 1,
                (5, 0): -2,
                (5, 2): 3,
                (5, 4): 4,
            },
            b={
                (0, 1): 1,
                (2, 1): 3,
                (2, 3): 1,
                (4, 3): 5,
                (5, 2): 9,
            }
        ),
        dict(
            a=[
                5, -5, -1, -6, -1, -6, 3, 11,
            ],
            c = {
                (0, 1): 8,
                (0, 7): 3,
                (1, 2): 2,
                (1, 6): 9,
                (2, 5): 4,
                (3, 2): -2,
                (3, 5): 1,
                (4, 3): 8,
                (5, 4): 4,
                (6, 2): 11,
                (6, 4): 6,
                (6, 5): 2,
                (7, 6): 5,
                (7, 5): 5,
            },
            b={
                (0, 1): 5,
                (0, 7): 0,
                (4, 3): 6,
                (6, 2): 1,
                (6, 4): 7,
                (7, 5): 6,
                (7, 6): 5,
            }
        )
    ]

    for i, case in enumerate(cases):
        web = Web(case['a'], case['c'])
        flow = web.min_cost_flow(case['b'])
        cost = sum(case['c'][e] * flow[e] for e in flow)
        print '#{}: cost = {}, flow = {}'.format(i, cost, flow)


if __name__ == '__main__':
    main()