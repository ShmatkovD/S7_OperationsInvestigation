# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from simplex import Simplex
import numpy as np


class BranchesMethod(object):

    def __init__(self, c, a, b, bounds):
        self._simplex = Simplex()
        self._c = c
        self._a = a
        self._b = b
        self._bounds = bounds

    @staticmethod
    def is_integer(val, eps=1e-6):
        return True if abs((val + eps) // 1 - val) < eps else False

    def solve_simplex(self, c, a, b, bounds):
        try:
            d_low = [i[0] for i in bounds]
            d_top = [i[1] for i in bounds]
            Jb = self._simplex.get_allowable_plan(c[:], a[:], b[:], d_low[:], d_top[:])
            res, Jb = self._simplex.solve(c[:], a[:], b[:], d_low[:], d_top[:], Jb[:])
            return res
        except Exception as e:
            pass

    def solve(self):
        eps = 1e-6
        r = -np.inf
        mu0 = False
        mu = np.zeros(len(self._c))

        queue = []
        queue.append(self._bounds)
        while queue:
            bounds = queue.pop(0)
            x = self.solve_simplex(self._c, self._a, self._b, bounds)
            if x is None:
                continue

            if any(not self.is_integer(coeff) for coeff in x):
                if np.dot(x, self._c) < r:
                    continue

            for i in range(len(x)):
                if not self.is_integer(x[i]):
                    l = x[i]
                    bounds_1, bounds_2 = bounds[:], bounds[:]
                    bounds_1[i] = [bounds[i][0], int(l)]
                    bounds_2[i] = [int(l) + 1, bounds[i][1]]
                    queue.append(bounds_1)
                    queue.append(bounds_2)
                    break
            else:
                continue

            new_r = np.dot(x, self._c)
            if new_r > r:
                mu, mu0, r = x, True, new_r

        return mu if mu0 == True else None


def main():
    c = [7, -2, 6, 0, 5, 2]
    b = [-8, 28, 30]
    bounds = [[2, 6], [1, 6], [0, 5], [0, 2], [1, 4], [1, 6]]
    a = [[1, -5, 3, 1, 0, 0],
         [4, -1, 1, 0, 1, 1],
         [2, 4, 2, 0, 0, 1]]

    method = BranchesMethod(c, a, b, bounds)
    ans = method.solve()

    print 'x = {}'.format(ans)
    if ans is not None:
        print "cx = {}".format(np.dot(ans, c))


if __name__ == '__main__':
    main()