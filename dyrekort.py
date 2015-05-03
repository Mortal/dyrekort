"""
Solution to the n balls in k bins for fixed k and variable n.
Requires the arbitrary precision integers of Python 3.
"""

import time
import itertools

import matplotlib.pyplot as plt


def prob(ns, k):
    """[(n, {n balls in k bins}) for n in `ns`]

    Computes the probability of all k bins being occupied after throwing
    n balls into them for n in ns.

    Generates a list of tuples (n, probability), where each probability
    is a Fraction.
    """

    B = binomial(k)
    numerators = [
        (-1) ** j * B[k][j]
        for j in range(k + 1)
    ]
    denominator = 1
    prev = 0
    for n in ns:
        skip = n - prev
        for i in range(len(numerators)):
            numerators[i] *= (k - i) ** skip
        denominator *= k ** skip
        prev = n
        yield n, Fraction(sum(numerators), denominator)


def binomial(N):
    """Returns B such that B[n][k] = n choose k for 0 <= n, k <= N"""
    B = []
    for n in range(N + 1):
        B.append((N + 1) * [0])
        for k in range(N + 1):
            # n choose k
            if k == 0 or k == n:
                B[n][k] = 1
            elif n == 0:
                B[n][k] = 0
            else:
                B[n][k] = B[n - 1][k] + B[n - 1][k - 1]
    return B


class Fraction(object):
    def __init__(self, a, b):
        d = self.gcd(a, b)
        self.a = divmod(a, d)[0]
        self.b = divmod(b, d)[0]

        # The largest float has exponent=1023 and mantissa=all 1's
        maxfloat = sum(2 ** i for i in range(1023 - 52, 1023 + 1))
        approx_numerator = divmod(self.a * maxfloat, self.b)[0]
        self.a_over_b = approx_numerator / maxfloat

    @staticmethod
    def gcd(a, b):
        """Euclid's algorithm to compute the greatest common divisor"""
        while b != 0:
            a, b = b, a % b
        return a


def main():
    k = 140
    data = []
    n_max = None
    i = 0
    t0 = time.time()
    for n, result in prob(itertools.count(), k):
        data.append((n, result.a_over_b))

        i += 1
        if i == 10:
            print('%6d:\t%s' %
                  (data[-i][0],
                   ''.join('%6.2f%%' % (100 * p,) for n, p in data[-i:])))
            i = 0

        if result.a_over_b > 0.5:
            if n_max is None:
                n_max = 2 * n
            elif n >= n_max:
                break

    if i != 0:
        print('%6d:\t%s' %
              (data[-i][0],
               ''.join('%6.2f%%' % (100 * p,) for n, p in data[-i:])))

    t1 = time.time()
    print('Time taken: %.4f s' % (t1 - t0,))
    xs, ys = zip(*data)
    plt.plot(xs, ys)
    plt.xlabel('Antal dyrekort')
    plt.ylabel('Sandsynlighed for at have alle %d' % k)
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
