import time
import operator


def binomial(N):
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


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def reduce(f, A):
    A = list(A)  # make copy
    n = len(A)
    while n > 1:
        n, d = divmod(n, 2)
        for i in range(n):
            # s = 'f(%s,%s) = ' % (A[2*i], A[2*i + 1])
            A[i] = f(A[2*i], A[2*i + 1])
            # print("%s%s" % (s, A[i]))
        if d:
            A[n] = A[2*n]
            n += 1
    return A[0]


def multi_gcd(A):
    return reduce(gcd, A)


def product(A):
    return reduce(operator.mul, A)


def timer(label):
    t0 = time.time()
    def next(s):
        nonlocal label
        nonlocal t0
        t1 = time.time()
        print("%-20s %7.4f s" % (label + ':', t1 - t0))
        label = s
        t0 = t1
    return next


def reduce_fraction(a, b):
    d = gcd(a, b)
    a = divmod(a, d)[0]
    b = divmod(b, d)[0]
    return a, b


class Fraction(object):
    def __init__(self, a, b):
        self.a, self.b = reduce_fraction(a, b)
        try:
            self.a_over_b = float(self.a) / float(self.b)
        except OverflowError:
            precision = 2 ** 50
            approx_numerator = divmod(self.a * precision, self.b)[0]
            self.a_over_b = approx_numerator / float(precision)


def prob(balls, bins):
    # t = timer('binomial')
    t = lambda s: None
    B = binomial(bins)
    t('factors')
    factors = [
        (-1) ** j * B[bins][j]
        for j in range(bins + 1)
    ]
    t('numerators')
    numerators = [
        factor * (bins - j) ** balls
        for j, factor in enumerate(factors)
    ]
    t('denominators')
    denominator = bins ** balls
    t('result')
    result = Fraction(sum(numerators), denominator)
    t('')
    return result


def main():
    # n = 743
    # range(0, 1000): 15.9965
    k = 140
    t0 = t1 = time.time()
    for n in range(0, 1000):
        result = prob(n, k)
        t2 = time.time()
        print('%d\t%7.4f\t%s' % (n, t2 - t1, result.a_over_b))
        t1 = t2
    print('Total\t%7.4f' % (t2 - t0,))


if __name__ == "__main__":
    main()
