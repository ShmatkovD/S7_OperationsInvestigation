# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from max_flow import Web
from copy import deepcopy


class Appointer(object):

    def __init__(self, c):
        self._c = c
        self._n = len(c)

    def appoint(self):
        c = deepcopy(self._c)

        for i in range(self._n):
            m = min(c[i])
            for j in range(self._n):
                c[i][j] -= m

        for i in range(self._n):
            m = float('inf')
            for j in range(self._n):
                m = min(m, c[j][i])
            for j in range(self._n):
                c[j][i] -= m

        while True:
            s = 2 * self._n
            t = 2 * self._n + 1
            e = {}

            for i in xrange(self._n):
                e[s, i] = 1
                e[i + self._n, t] = 1

            for i in range(self._n):
                for j in range(self._n):
                    if c[i][j] == 0:
                        e[i, j + self._n] = float('inf')

            web = Web(2 * self._n + 2, e, s, t)
            f = web.get_flow()
            if sum(f[s]) == self._n:
                result = []
                for i in xrange(self._n):
                    for j in xrange(self._n):
                        if f[i][j + self._n] > 0:
                            result.append((i, j))
                return result

            n1, nn1, n2, nn2 = [], [], [], []
            for i in xrange(self._n):
                if web.used[i]:
                    n1.append(i)
                else:
                    nn1.append(i)
                if web.used[i + self._n]:
                    n2.append(i)
                else:
                    nn2.append(i)

            alpha = min(c[i][j] for i in n1 for j in nn2 if c[i][j] != 0)
            for i in n1:
                for j in nn2:
                    c[i][j] -= alpha

            for i in nn1:
                for j in n2:
                    c[i][j] += alpha


def main():
    inf = float('inf')
    cases = [
        [
            [inf, 10, 25, 25, 10],
            [1, inf, 10, 15, 2],
            [8, 9, inf, 20, 10], [14, 10, 24, inf, 15],
            [10, 8, 25, 27, inf]
        ],
        [
            [2, 10, 9, 7],
            [15, 4, 14, 8],
            [13, 14, 16, 11],
            [4, 15, 13, 19]
        ],
        [
            [6, 4, 13, 4, 19, 15, 11, 8],
            [17, 15, 18, 14, 0, 7, 18, 7],
            [3, 5, 11, 9, 7, 7, 18, 16],
            [17, 10, 16, 19, 9, 6, 1, 5],
            [14, 2, 10, 14, 11, 6, 4, 10],
            [17, 11, 17, 12, 1, 10, 6, 19],
            [13, 1, 4, 2, 2, 7, 2, 14],
            [12, 15, 19, 11, 13, 1, 7, 8]
        ],
        [
            [9, 6, 4, 9, 3, 8, 0],
            [5, 8, 6, 8, 8, 3, 5],
            [5, 2, 1, 1, 8, 6, 8],
            [1, 0, 9, 2, 5, 9, 2],
            [9, 2, 3, 3, 0, 3, 0],
            [7, 3, 0, 9, 4, 5, 6],
            [0, 9, 6, 0, 8, 8, 9]
        ],
        [
            [6, 6, 2, 4, 7, 1, 9, 4, 6],
            [5, 0, 2, 4, 9, 2, 9, 2, 0],
            [7, 6, 0, 5, 2, 3, 0, 5, 5],
            [9, 5, 8, 9, 2, 3, 1, 5, 7],
            [3, 1, 7, 3, 0, 2, 2, 8, 1],
            [3, 0, 0, 6, 1, 7, 2, 4, 7],
            [5, 6, 1, 9, 9, 8, 4, 1, 8],
            [5, 4, 5, 2, 2, 6, 6, 5, 6],
            [3, 6, 1, 6, 3, 0, 5, 2, 2]],

        [
            [2, 4, 0, 3, 8, -1, 6, 5],
            [8, 6, 3, 4, 2, 0, 0, 4],
            [8, -4, 3, 2, 7, 3, 1, 0],
            [2, 4, 9, 5, 3, 0, 3, 8],
            [5, 2, 7, 3, -1, 0, 3, 2],
            [3, 2, 5, 1, 5, 3, 0, 1],
            [2, 1, 0, -3, 1, 2, 7, 0],
            [1, 6, 4, 0, 0, 9, 1, 7]
        ],
    ]

    for i, case in enumerate(cases):
        appointer = Appointer(case)
        result = appointer.appoint()
        cost = sum(case[i][j] for i, j in result)
        print '#{}: cost = {}, appointments = {}'.format(i, cost, result)


if __name__ == '__main__':
    main()