# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class Web(object):

    def __init__(self, n, e, s, t):
        self._n = n
        self._s = s
        self._t = t
        self._g, self._c = self.prepare(e)
        self.used = []

    def prepare(self, e):
        g = [[] for _ in range(self._n)]
        c = [[-1] * self._n for _ in range(self._n)]
        for (i, j), flow in e.items():
            c[i][j] = flow
            g[i].append(j)
        return g, c

    def find_path(self, f):
        self.used = [False] * self._n
        prev = [-1] * self._n
        queue = [self._s]
        while queue:
            i = queue.pop(0)
            for j in self._g[i]:
                if not self.used[j] and self._c[i][j] - f[i][j] > 0:
                    self.used[j] = True
                    prev[j] = i
                    queue.append(j)

        path = []
        i = self._t
        while prev[i] != -1:
            path.append((prev[i], i))
            i = prev[i]
        return path

    def get_flow(self):
        f = [[0] * self._n for _ in xrange(self._n)]
        while True:
            path = self.find_path(f)
            if not path:
                return f
            else:
                flow = float('inf')
                for i, j in path:
                    flow = min(flow, self._c[i][j] - f[i][j])

                for i, j in path:
                    f[i][j] += flow
                    f[j][i] -= flow


if __name__ == '__main__':
    cases = [
        dict(n=10, s=0, t=9, e={
            (0, 1): 4,
            (0, 3): 9,
            (1, 3): 2,
            (1, 4): 4,
            (3, 2): 1,
            (3, 5): 6,
            (2, 4): 1,
            (2, 5): 10,
            (4, 5): 1,
            (4, 9): 2,
            (5, 9): 7,
        }),
        dict(n=7, s=0, t=6, e={
            (0, 1): 4,
            (0, 3): 9,
            (1, 3): 2,
            (1, 4): 4,
            (2, 4): 1,
            (2, 5): 10,
            (3, 2): 1,
            (3, 5): 6,
            (4, 5): 1,
            (4, 6): 2,
            (5, 6): 9
        }),
        dict(n=8, s=0, t=7, e={
            (0, 1): 3,
            (0, 2): 2,
            (0, 3): 1,
            (0, 5): 6,
            (1, 3): 1,
            (1, 4): 2,
            (2, 3): 1,
            (2, 4): 2,
            (2, 5): 4,
            (3, 4): 7,
            (3, 6): 4,
            (3, 7): 1,
            (3, 5): 5,
            (4, 6): 3,
            (4, 7): 2,
            (5, 7): 4,
            (6, 7): 5,
            (6, 5): 3
        })
    ]

    for i, case in enumerate(cases):
        web = Web(**case)
        f = web.get_flow()
        print '#{}: max flow = {}'.format(i, sum(f[case['s']]))