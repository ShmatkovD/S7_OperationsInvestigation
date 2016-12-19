# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import numpy as np
from numpy.linalg import inv
from scipy.optimize import linprog


class Simplex(object):

    def get_not_basis(self, n, J):
        res = []
        for i in range(n):
            if not i in J:
                res.append(i)
        return np.array(res)

    def reshuffle(self, set, rem, inc):
        res = set[:]
        res[res.index(rem)] = inc
        return res

    def get_j0(self, A):

        def rec(ans, vals):
            if len(vals) == m:
                if len(ans[0]) == 0 and abs(np.linalg.det(A[:, vals])) > 1e-9:
                    ans[0] = vals[:]
                return
            prev = vals[-1] if len(vals) > 0 else -1
            for i in range(prev + 1, n):
                tvals = vals[:]
                tvals.append(i)
                rec(ans, tvals)

        m, n = len(A), len(A[0])
        ans = {}
        ans[0] = []
        rec(ans, [])
        return ans[0]

    def inverse_matrix(self, A_b, A_inv_B, theta0_ind):
        l = np.dot(A_inv_B, A_b[:, theta0_ind])
        l_tilda = l.copy()
        l_tilda[theta0_ind] = -1
        q = np.dot((-1.0 / l[theta0_ind]), l_tilda)
        E = np.eye(A_b.shape[0])
        E[:, theta0_ind] = q
        return np.dot(E, A_inv_B)

    def solve(self, c, a, b, d_bot, d_top, Jb=None):
        eps = 1e-9
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        d_bot = np.array(d_bot)
        d_top = np.array(d_top)

        n, m = len(c), len(b)
        if Jb == None:
            Jb = self.get_j0(a)
        # print('Jb = ', Jb)
        Ab = a[:, Jb]
        # print('Ab = ', Ab)
        B = np.linalg.inv(Ab)
        y = np.dot(c[Jb], B)
        delta = np.dot(y, a) - c
        Jn = self.get_not_basis(n, Jb)
        Jn_plus, Jn_minus = [], []
        for i in Jn:
            if delta[i] >= 1e-9:
                Jn_plus.append(i)
            else:
                Jn_minus.append(i)
        K = 1e5
        while K > 0:
            # print(K)
            K -= 1
            # create xi
            xi = np.zeros(n)
            for i in Jn_plus:
                xi[i] = d_bot[i]
            for i in Jn_minus:
                xi[i] = d_top[i]
            sm = np.zeros(m)
            for i in Jn:
                sm += np.dot(a[:, i], xi[i])
            dxi = np.dot(B, b - sm)
            for v, i in enumerate(Jb):
                xi[i] = dxi[v]
                # check
            ok = True
            for i in Jb:
                ok &= d_bot[i] - eps <= xi[i] <= d_top[i] + eps
            if ok:
                return xi, Jb  # return optimum X and Jb
            jk = np.inf
            for v, i in enumerate(Jb):
                if xi[i] < d_bot[i] - eps or xi[i] + eps > d_top[i]:
                    if jk > i:
                        jk, k = i, v
            mk = 1 if xi[jk] < d_bot[jk] else -1
            del_y = np.dot(mk, np.dot(np.eye(m, m)[:, k], B))
            mu = np.zeros(n)
            for i in Jn:
                mu[i] = np.dot(del_y, a[:, i])
            mu[jk] = mk
            # create sigma
            sigm = np.zeros(n)
            for i in Jn_plus:
                sigm[i] = -delta[i] / mu[i] if mu[i] < 0 else np.inf
            for i in Jn_minus:
                sigm[i] = -delta[i] / mu[i] if mu[i] > 0 else np.inf
            sigm0 = min(sigm[Jn])
            if sigm0 == np.inf:
                return None  # not limited
            for i in Jn:
                if sigm[i] == sigm0:
                    j0 = i
            for i in Jn:
                delta[i] += np.dot(sigm0, mu[i])
            delta[jk] = np.dot(sigm0, mu[jk])
            for i in Jb:
                if i != jk:
                    delta[i] = 0.0

                    # get new Jb, Jn, Jn_plus, Jn_minus, Ab
            Jb = self.reshuffle(Jb, jk, j0)
            Ab = a[:, Jb]
            Jn = self.get_not_basis(n, Jb)
            if mk == 1:
                if j0 in Jn_plus:
                    Jn_plus.remove(j0)
                    Jn_plus.append(jk)
                else:
                    Jn_plus.append(jk)
            if mk == -1:
                if j0 in Jn_plus:
                    Jn_plus.remove(j0)
            Jn_minus = []
            for i in Jn:
                if not i in Jn_plus:
                    Jn_minus.append(i)
                    # get new inverse Ab using Kostukova special
            z = np.dot(B, Ab[:, k])
            d = z.copy()
            d[k] = -1
            q = np.dot(-(1.0 / z[k]), d)
            E = np.eye(m, m)
            E[:, k] = q.copy()
            B = np.dot(E, B)
            # print(Jb)
        return None

    def get_allowable_plan(self, C, A, b, d_bot, d_top):
        b = np.array(b)
        A = np.array(A)
        C = np.array(C)
        if (b < 0).any():
            subinds = b < 0
            b[subinds] *= -1
            A[subinds, :] *= -1

        m = len(A)
        n = len(A[0]) - m
        real_inds = [i for i in range(n)]
        synth_inds = [i for i in range(n, n + m)]

        X = self.solve(C[:], A[:], b[:], d_bot[:], d_top[:], synth_inds[:])
        if X is None:
            raise Exception('The task is inconsistent')
        X, B = X
        not_base_real_inds = np.array(list(set(real_inds) - set(B)))

        if B not in synth_inds:
            return B
        B.sort()
        k = 0
        while k < len(B):
            ind = B[k]
            if ind in synth_inds:
                A_inv_b = inv(extended_A[:, B])
                is_found = False
                for j in not_base_real_inds:
                    l = np.dot(A_inv_b, A[:, j])

                    if l[k] != 0:
                        B[k] = j
                        is_found = True
                        break
                if not is_found:
                    i = ind - n
                    A = np.delete(A, k, axis=0)
                    extended_A = np.delete(extended_A, k, axis=0)
                    b = np.delete(b, k)
                    for t, s_ind in enumerate(synth_inds):
                        if s_ind == ind:
                            synth_inds = np.delete(synth_inds, t)
                            break
                    B = np.delete(B, k)
                    continue
            k += 1
        return B