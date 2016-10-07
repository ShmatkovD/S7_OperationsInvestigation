import numpy

FILENAME = 'input.txt'


def read():
    with open(FILENAME, 'r') as f:
        n, m = [int(item) for item in f.readline().split(' ')]

        A = numpy.matrix(
            [
                [float(item) for item in f.readline().split(' ')[:n]]
                for _ in xrange(m)
            ]
        )

        b = numpy.matrix([
            [float(item)] for item in f.readline().split(' ')[:m]
        ])

        c = numpy.matrix([
            [float(item)] for item in f.readline().split(' ')[:n]
        ])

        d_l = numpy.array([
            [float(item)] for item in f.readline().split(' ')[:n]
        ])

        d_u = numpy.array([
            [float(item)] for item in f.readline().split(' ')[:n]
        ])

        j_basis = {i + (n - m) for i in xrange(m)}

        return n, m, A, b, c, d_u, d_l, j_basis


def run():
    n, m, A, b, c, d_u, d_l, j_basis = read()

    A_basis = A[:, sorted(j_basis)]
    B = A_basis.I

    # 1
    c_a = c[sorted(j_basis)]
    y = c_a.T.dot(B)

    deltas = numpy.array(
        [(y.dot(A[:, [j]]) - c[j, :])[0, 0] for j in range(n)]
    )

    j_nb = set(range(n)) - j_basis

    j_nbp = {item for item in j_nb if deltas[item] > 0}
    j_nbm = j_nb - j_nbp

    while True:

        # 2
        xi_nb = dict(
            (i, numpy.matrix(d_l[i]))
            if i in j_nbp else
            (i, numpy.matrix(d_u[i]))
            for i in j_nb
        )

        xi_b = B.dot(
            b - sum([
                A[:, [j]].dot(xi_nb[j]) for j in j_nb
            ])
        )

        xi = {
            item: xi_b[i] for i, item in enumerate(sorted(j_basis))
        }
        xi.update(xi_nb)

        xi = numpy.array([
            item[0, 0] for i, item in sorted(
                list(xi.items()),
                key=lambda x: x[0],
            )
        ])

        # 3. Exit when solution found
        wrong_items = [
            i for i in xrange(n)
            if not(d_l[i] <= xi[i] <= d_u[i])
        ]

        if not wrong_items:
            return xi, c.T.dot(xi)

        # 4
        j_k = wrong_items[0]

        # 5
        mu_jk = 1
        e_k = numpy.array([
            1 if i == j_k else 0
            for i in sorted(j_basis)
        ])

        delta_y = (mu_jk * e_k).dot(B)

        mu = delta_y.dot(A)

        i = 1
        # 6

        func = lambda j: float(-deltas[j]) / (float(mu[0, j]) or 1) if (
            (
                (j in j_nbp) and (mu[0, j] < 0)
            ) or (
                (j in j_nbm) and (mu[0, j] > 0)
            )
        ) else float('inf')

        r = func(1)

        sigmas = [
            -deltas[j] / mu[0, j] if (
                (
                    (j in j_nbp) and (mu[0, j] < 0)
                ) or (
                    (j in j_nbm) and (mu[0, j] > 0)
                )
            ) else float('inf')
            for j in sorted(j_nb)
        ]

        sigma_zero = min(sigmas)

        if sigma_zero == float('inf'):
            return 'No solutions'

        sigma_pos = sorted(j_nb)[sigmas.index(sigma_zero)]

        # 7
        deltas = [deltas[j] + sigma_zero * mu[0, j] for j in xrange(n)]

        # 8
        j_basis = j_basis - {j_k} | {sigma_pos}

        B = A[:, sorted(j_basis)].I

        # 9
        j_nb = {j for j in xrange(n)} - j_basis

        if sigma_pos in j_nbp:
            j_nbp -= {sigma_pos}
        if mu_jk:
            j_nbp |= {j_k}

        j_nbm = j_nb - j_nbp


if __name__ == '__main__':
    result = run()

    print result
