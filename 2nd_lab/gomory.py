# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import numpy as np
from simplex import Simplex


class GomoryMethod(object):

    inf = float('inf')

    def __init__(self, c, a, b, bounds):
        self._simplex = Simplex()
        self._c = c
        self._a = a
        self._b = b
        self._bounds = bounds

    @staticmethod
    def is_integer(val, eps=1e-9):
        return abs((val + eps) // 1 - val) < eps

    def solve_simplex(self, c, a, b, bounds, Jb=None):
        try:
            b_b = [i[0] for i in bounds]
            b_u = [i[1] for i in bounds]
            x, Jb = self._simplex.solve(c, a, b, b_b, b_u)
            return (x, Jb) if not x is None else (None, None)
        except Exception as e:
            print e
            return None, None

    def del_synth(self, a, b, c, bounds, Jb, i0, delt):
        i0 -= delt
        ai = a[i0][:]
        bi = b[i0]
        koefs = []
        for i in range(len(ai)):
            koefs.append(ai[i] / a[i0][i0 + delt])
        for i in range(i0 + 1, len(b)):
            b[i] -= bi / a[i0][i0 + delt] * a[i][i0 + delt]
        for i in range(len(a)):
            for j in range(len(a[i])):
                if j != i0 + delt:
                    a[i][j] -= a[i][i0 + delt] * koefs[j]
        _b = []
        for i in range(len(b)):
            if i != i0:
                _b.append(b[i])
        _a = []
        for v, i in enumerate(a):
            t = []
            if v == i0:
                continue
            for j in range(len(i)):
                if j != i0 + delt:
                    t.append(i[j])
            _a.append(t)
        a = np.array(_a)
        b = np.array(_b)
        c = c[:-1]
        bounds = bounds[:-1]
        _Jb = []
        for i in Jb:
            if i == i0 + delt:
                continue
            if i > i0 + delt:
                _Jb.append(i - 1)
            if i < i0 + delt:
                _Jb.append(i)
        Jb = _Jb
        return a, b, c, bounds, Jb

    def solve(self):
        a = np.array(self._a[:])
        b = np.array(self._b[:])
        c = np.array(self._c[:])
        bounds = np.array(self._bounds[:]).tolist()

        cur = 1
        n, m = len(c), len(b)
        eps = 1e-9
        while True:
            x, Jb = self.solve_simplex(c, a, b, bounds)
            if x is None:
                return None

            for i in range(n, len(a)):
                if i in Jb:
                    a, b, c, bounds, Jb = self.del_synth(a[:], b[:], c[:], bounds[:], Jb[:], i, n - m)
                    x, Jb = self.solve_simplex(c, a, b, bounds)

            ok = True
            for i in range(n):
                ok &= self.is_integer(x[i])
            if ok:
                return x[:n]

            for v, i in enumerate(Jb):
                if not self.is_integer(x[i]):
                    k = v
                    break
            Ab = a[:, Jb]
            B = np.linalg.inv(Ab)

            ej0 = np.eye(len(Jb), len(Jb))[:, k]
            y = np.dot(ej0, B)
            betta = np.dot(y, b)
            alpha = np.dot(y, a)
            row = [- (i - int(i)) for i in alpha]
            row.append(1)
            temp = a.tolist()
            temp.append(row)
            a = np.array(temp)

            b = np.append(b, -(betta - int(betta)))
            bounds.append([0, self.inf])
            c = np.append(c, 0)
            cur += 1


def main():
    c = [7, -2, 6, 0, 5, 2]
    b = [-8, 28, 30]
    bounds = [[2, 6], [1, 6], [0, 5], [0, 2], [1, 4], [1, 6]]
    a = [[1, -5, 3, 1, 0, 0],
         [4, -1, 1, 0, 1, 1],
         [2, 4, 2, 0, 0, 1]]

    method = GomoryMethod(c, a, b, bounds)
    x = method.solve()
    print(x)
    print(np.dot(x, c))


if __name__ == '__main__':
    main()