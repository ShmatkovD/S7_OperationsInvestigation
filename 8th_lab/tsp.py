# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from copy import deepcopy

import numpy as np
from appointing import Appointer

inf = np.inf


class TSP(object):

    def __init__(self, c):
        self._c = c
        self._n = len(c)

    @staticmethod
    def find_cycles(res):
        cycles = []
        used = [False for i in range(len(res))]
        for v in range(len(res)):
            if used[v]:
                continue
            cur, cycle, used[v] = res[v][1], [v], True
            while cur != v:
                cycle.append(cur)
                used[cur] = True
                cur = res[cur][1]
            cycle.append(v)
            cycles.append(cycle)
        return cycles

    def removing_sub_cycles(self):
        c, n = deepcopy(self._c), self._n
        opt_path = [i for i in range(n)] + [0]
        opt = sum(c[opt_path[i]][opt_path[i + 1]] for i in range(n))

        queue = []
        queue.append(c)
        while queue:
            c = queue.pop(0)
            appointer = Appointer(c)
            res = appointer.appoint()
            cur_cost = sum(c[i][j] for i, j in res)
            if cur_cost >= opt:
                continue
            else:
                cycles = self.find_cycles(res)
                if len(cycles) == 1:
                    path = cycles[0]
                    cur_ans = sum(c[path[i]][path[i + 1]] for i in range(n))
                    if cur_ans < opt:
                        opt, opt_path = cur_ans, path
                else:
                    min_cycle = min(cycles, key=lambda c: len(c))
                    for i in range(len(min_cycle) - 1):
                        new_c = deepcopy(c)
                        new_c[min_cycle[i]][min_cycle[(i + 1) % len(min_cycle)]] = inf
                        queue.append(new_c)
        return opt_path

    @staticmethod
    def get_pos(c, x=(), y=()):
        n, x, y = set(xrange(len(c))), set(x), set(y)
        for i in n - x:
            for j in n - y:
                if c[i][j] != inf:
                    return i, j

    @staticmethod
    def get_lower_cost(c, x, y):
        cost = sum(c[x[i]][y[i]] for i in range(len(x)))
        n, x, y = set(xrange(len(c))), set(x), set(y)
        c = deepcopy(c)
        for i in n - x:
            mn = min(c[i][j] for j in n - y)
            cost += mn
            for j in n - y:
                c[i][j] -= mn
        for i in n - y:
            cost += min(c[j][i] for j in n - x)
        return cost

    def solve(self, opt, opt_path, c, x, y):
        lower_cost = self.get_lower_cost(deepcopy(c), x, y)
        if lower_cost >= opt:
            return opt, opt_path
        elif len(x) == self._n - 1:
            opt = lower_cost
            opt_path = deepcopy(x) + [y[-1], x[0]]
            return opt, opt_path
        else:
            new_x = y[-1] if len(y) != 0 else 0
            for new_y in range(self._n):
                if new_y in x or new_y in y:
                    continue
                elif c[new_x][new_y] != inf:
                    c1, c2 = deepcopy(c), deepcopy(c)
                    c2[new_x][new_y] = inf
                    x1, x2, y1, y2 = deepcopy(x), deepcopy(x), deepcopy(y), deepcopy(y)
                    x1.append(new_x)
                    y1.append(new_y)
                    opt, opt_path = self.solve(opt, opt_path, c1, x1, y1)
                    opt, opt_path = self.solve(opt, opt_path, c2, x2, y2)
                    return opt, opt_path
        return opt, opt_path

    def set_routes(self):
        kp = self.get_pos(self._c)
        c1, c2 = deepcopy(self._c), deepcopy(self._c)
        c2[kp[0]][kp[1]] = inf
        opt, opt_path = self.solve(float('inf'), [], c1, [kp[0]], [kp[1]])
        opt, opt_path = self.solve(opt, opt_path, c2, [], [])
        return opt_path


def main():
    cases = [
        [
            [inf, 10, 25, 25, 10],
            [1, inf, 10, 15, 2],
            [8, 9, inf, 20, 10],
            [14, 10, 24, inf, 15],
            [10, 8, 25, 27, inf]
        ],
        [
            [inf, 2, 1, 10, 6],
            [4, inf, 3, 1, 3],
            [2, 5, inf, 8, 4],
            [6, 7, 13, inf, 3],
            [10, 2, 4, 6, inf]
        ],
        [
            [inf, 27, 43, 16, 30, 26],
            [7, inf, 16, 1, 30, 30],
            [20, 13, inf, 35, 5, 0],
            [21, 16, 25, inf, 18, 18],
            [12, 46, 27, 48, inf, 5],
            [23, 5, 5, 9, 5, inf]
        ],
    ]

    for i, case in enumerate(cases):
        print "#{}:".format(i)
        res = TSP(case).removing_sub_cycles()
        cost = sum(case[res[i]][res[i + 1]] for i in range(len(res) - 1))
        print "Removing sub cycles: {}".format(cost)

        res = TSP(case).set_routes()
        cost = sum(case[res[i]][res[i + 1]] for i in range(len(res) - 1))
        print "Route setting: {}\n".format(cost)


if __name__ == '__main__':
    main()