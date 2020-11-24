from Cryptodome.Random.random import randint as randint_range
from Cryptodome.Util.number import getRandomInteger as randint_bits, getPrime as random_prime

from random import sample

from lab4.aes_tests import current_ms, duration_ms


def max_of_nbit(n: int) -> int:
    """ Integer value from n times '1' in number's binary representation.
    """
    return int('1' * n, 2)


def neg_mod(num: int, value: int) -> int:
    """ Negative modulus to standard output.
        Example: `neg_mod(-5, 4) == 1`
    """
    return num - int(num / value) * value


def polynomial(x: int, coeff: [int]) -> int:
    """ Calculates the value of a polynomial with coefficients in given order.
    """
    return sum([x ** (len(coeff) - i - 1) * coeff[i] for i in range(len(coeff))])


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
    def split(secret: int, n: int, t: int, p: int = None, prime_bit_size: int = 16) -> ([int], int):
        if not p:
            while (p := random_prime(prime_bit_size)) <= secret and p <= n: pass

        # a = [randint_range(0, p) for _ in range(t - 1)]
        a = [62, 352]

        s = []
        for i in range(1, n + 1):
            total = 0
            a_index = 0
            for power in reversed(range(1, t)):
                total += a[a_index] * (i ** power)
                a_index += 1

            s.append((i, (total + secret) % p))

        return s, p

    @staticmethod
    def merge(s: [(int, int)], p: int):
        factors = []

        for xj, yj in s:
            top = 1
            bottom = 1

            for xi, _ in s:
                if xj == xi: continue

                top *= -xi
                bottom *= (xi - xj)

            if neg_mod(top, bottom) == 0:
                value = top // bottom

            else:
                value = 1
                while value * bottom % p != top:
                    value += 1

            factors.append(neg_mod(value * yj, p))

        return sum(factors)

    @staticmethod
    def test():
        secret = 954
        p = 1523
        n = 4
        t = 3

        for _ in range(1000):
            split, p = Schamir.split(secret, n, t, p=p)

            pool = sample(split, t)

            merged = Schamir.merge(pool, p)

            if secret != merged:
                print(f"failed with {pool=}\n{merged=}")
        else:
            print("ok")


class WorkingSchamir:
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

        x = WorkingSchamir.split(n, t, secret)

        pool = sample(x, t)
        y = WorkingSchamir.merge(pool)

        print(f"{pool=} | {y=}")

        assert secret == y


if __name__ == '__main__':
    # Trivial.test()
    # Schamir.test()
    WorkingSchamir.test()
