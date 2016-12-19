# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from copy import deepcopy

inf = float('inf')


class Floyd(object):

    __inf = float('inf')

    def __init__(self, a, n):
        self._a = a
        self._n = n

    def destinations(self):
        d = deepcopy(self._a)
        p = [[i for i in xrange(self._n)] for j in xrange(self._n)]
        for k in xrange(self._n):
            for i in xrange(self._n):
                for j in xrange(self._n):
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        p[i][j] = k
        return d, p

    def paths(self):
        d, p = self.destinations()
        paths = [[None for i in xrange(self._n)] for j in xrange(self._n)]
        for i in xrange(self._n):
            for j in xrange(self._n):
                if d[i][j] != self.__inf:
                    current, path = i, [i]
                    while current != j:
                        current = p[current][j]
                        path.append(current)
                    paths[i][j] = path
        return paths


def main():
    i = float('inf')
    n = 8
    a = [
        [0, 9, i, 3, i, i, i, i],
        [9, 0, 2, i, 7, i, i, i],
        [i, 2, 0, 2, 4, 8, 6, i],
        [3, i, 2, 0, i, i, 5, i],
        [i, 7, 4, i, 0, 10, i, i],
        [i, i, 8, i, 10, 0, 7, i],
        [i, i, 6, 5, i, 7, 0, i],
        [i, i, i, i, 9, 12, 10, 0]
    ]

    floyd = Floyd(a, n)
    d, r = floyd.destinations()
    p = floyd.paths()
    print d
    print r
    print p[4][0]
    print p[0][4]
    print p[0][7]


if __name__ == '__main__':
    main()