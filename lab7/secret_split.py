from random import sample
from math import fmod

from Cryptodome.Random.random import randint as randint_range
from Cryptodome.Util.number import getRandomInteger as randint_bits, getPrime as random_prime

from lab4.aes_tests import current_ms, duration_ms
from lab6.rsa import extended_gcd


def max_of_nbit(n: int) -> int:
    """ Integer value from n times '1' in number's binary representation.
    """
    return int('1' * n, 2)


def neg_mod(num: int, value: int) -> int:
    """ Negative modulus to standard output.
        Example: `neg_mod(-5, 4) == 1`
    """
    return num - int(num / value) * value


def polynomial(x: int, coeffs: [int]) -> int:
    """ Calculates the value of a polynomial with coefficients in given order.
    """
    return sum([x ** (len(coeffs) - i - 1) * coeffs[i] for i in range(len(coeffs))])


def inv_mod(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m


def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def div_mod(num, den, p):
    """Compute num / den modulo prime p

    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv


class Trivial:
    @staticmethod
    def split(secret: int, k: int, n: int) -> [int]:
        s = [randint_range(0, k - 1) for _ in range(n - 1)]
        sn = (secret - sum(s)) % k

        return s + [sn]

    @staticmethod
    def merge(s: [int], k: int) -> int: return sum(s) % k

    @staticmethod
    def test() -> None:
        secret = randint_bits(128) - 1
        k = max_of_nbit(128)
        n = randint_range(10, 100)

        print(f"{secret=}, {k=}, {n=}")

        start = current_ms()
        split = Trivial.split(secret, k, n)
        print(f"split {duration_ms(start)=}[ms]")

        start = current_ms()
        merge = Trivial.merge(split, k)
        print(f"merge {duration_ms(start)=}[ms]")

        assert secret == merge

        print("secrets match")


class Schamir:
    @staticmethod
    def split(secret: int, n: int, t: int, p: int) -> ([int], int):
        a = [randint_range(0, 10) for _ in range(t - 1)] + [secret]

        return [(i, polynomial(i, a) % p) for i in range(1, n + 1)], p

    @staticmethod
    def merge(s: [(int, int)], p: int):
        factors = []

        for xj, yj in s:
            top = 1
            bottom = 1

            for xi, _ in s:
                if xj == xi: continue

                top *= xi
                bottom *= xi - xj

            value = div_mod(top, bottom, p)

            factors.append(neg_mod(value * yj, p))

        result = sum(factors)
        return result + p if result < 0 else result

    @staticmethod
    def test():
        secret = 954
        n = 4
        t = 3
        prime = 2 ** 127 - 1

        for _ in range(100):
            split, p = Schamir.split(secret, n, t, p=prime)

            pool = sample(split, t)

            merged = Schamir.merge(pool, p)

            if merged != secret:
                print(f"failed with {pool=} - {merged=} | {p=}")

            else:
                print(f"ok with {pool=} - {merged=} | {p=}")


class SimpleSchamir:
    @staticmethod
    def split(n: int, t: int, secret: int, rand_max: int = 10 ** 5) -> [(int, int)]:
        cfs = [randint_range(0, rand_max) for _ in range(t - 1)] + [secret]

        shares = []
        for i in range(1, n + 1):
            r = randint_range(1, rand_max)
            shares.append((r, polynomial(r, cfs)))

        return shares

    @staticmethod
    def merge(shares: [(int, int)]) -> int:
        sums = 0

        for xj, yj in shares:
            prod = 1
            for xi, _ in shares:
                if xi != xj: prod *= xi / (xi - xj)

            prod *= yj
            sums += prod

        return int(round(sums, 0))

    @staticmethod
    def test():
        secret = 954
        n = 4
        t = 3

        x = SimpleSchamir.split(n, t, secret)

        pool = sample(x, t)
        y = SimpleSchamir.merge(pool)

        print(f"{pool=} | {y=}")

        assert secret == y


if __name__ == '__main__':
    # Trivial.test()
    # Schamir.test()
    # WorkingSchamir.test()

    prime = 2 ** 127 - 1
    shares, _ = Schamir.split(1234152, 10, 5, prime)

    print(Schamir.merge(shares[5:], prime))
