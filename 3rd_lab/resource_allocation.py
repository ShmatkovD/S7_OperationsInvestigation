# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from copy import copy
from numpy import zeros


class ResourceAllocator(object):

    def __init__(self, f, c, n):
        self._f = f
        self._v = c + 1
        self._n = n

    def allocate(self):
        c = len(self._f[0])

        p = list(zeros((self._n, self._v)).tolist())
        for i in xrange(c):
            p[0][i] = i

        b = list(zeros((self._n, self._v)).tolist())
        for i in xrange(c):
            b[0][i] = self._f[0][i]

        for k in xrange(1, self._n):
            for y in xrange(1, self._v):
                for z in xrange(min(y + 1, c)):
                    if b[k][y] < self._f[k][z] + b[k - 1][y - z]:
                        b[k][y] = self._f[k][z] + b[k - 1][y - z]
                        p[k][y] = z

        x = [0] * self._n
        current = self._v - 1
        for k in range(0, self._n)[::-1]:
            x[k] = p[k][current]
            current -= p[k][current]
        return b[self._n - 1][self._v - 1], x


def main():
    cases = [
        {
            "c": 7,
            "n": 3,
            "f": [
                [0, 1, 2, 3, 4, 5],
                [0, 0, 1, 2, 4, 7],
                [0, 2, 2, 3, 3, 5],
            ]
        }
    ]

    f, c, n = cases[0]['f'], cases[0]['c'], cases[0]['n']
    allocator = ResourceAllocator(f, c, n)
    max_value, x = allocator.allocate()
    print('Ans = {}, X = {}'.format(max_value, x))


if __name__ == '__main__':
    main()