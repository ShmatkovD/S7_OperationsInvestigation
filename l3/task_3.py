import numpy as np


def solve(a, k):
    """
    :param a: matrix with cost
    :param k: count of resources
    """
    a = np.append(
        np.array([[0 for _ in xrange(a.shape[1])]]),
        a, 0
    )
    n, m = a.shape

    # f[i][j] - result; counts[i][j] - how many resources spent on this factory
    # i - factory, j - how many resources we already used
    # !!! Need to read !!! need to use k + 1 everywhere because numeration and
    # counting always starts from 0

    f = np.ndarray(shape=(n, k + 1))
    f.fill(0)
    counts = np.ndarray(shape=(n, k + 1), dtype=int)
    counts.fill(0)

    for current_factory in xrange(1, n):

        max_count = min(m, k + 1)
        for current_count in xrange(max_count):

            max_used_count = k + 1 - current_count
            for used_count in xrange(max_used_count):

                old_value = f[current_factory, current_count + used_count]
                new_value = (
                    f[current_factory - 1, used_count] +
                    a[current_factory, current_count]
                )
                if old_value < new_value:
                    f[current_factory, current_count + used_count] = new_value
                    counts[current_factory, current_count + used_count] = current_count

    result = -1
    used_count = -1
    for i in xrange(k + 1):
        if result < f[n - 1, i]:
            result = f[n - 1, i]
            used_count = i

    result_counts = []
    for current_factory in reversed(xrange(n)):
        result_counts.append(counts[current_factory, used_count])
        used_count -= counts[current_factory, used_count]

    result_counts = result_counts[:-1]

    return result, list(reversed(result_counts))

if __name__ == '__main__':
    a = np.array([
        [0, 4, 4, 6, 9, 12, 12, 15, 16, 19, 19, 19],
        [0, 1, 1, 1, 4, 7, 8, 8, 13, 13, 19, 20],
        [0, 2, 5, 6, 7, 8, 9, 11, 11, 13, 13, 18],
        [0, 1, 2, 4, 5, 7, 8, 8, 9, 9, 15, 19],
        [0, 2, 5, 7, 8, 9, 10, 10, 11, 14, 17, 21],
    ])

    k = 11
    result, vector = solve(a, k)

    print result
    print vector
