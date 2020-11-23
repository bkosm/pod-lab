from math import prod

from Cryptodome.Random.random import randint as randint_range
from Cryptodome.Util.number import getRandomInteger as randint_bits, getStrongPrime as random_prime

from scipy.interpolate import lagrange
from numpy import array

from lab4.aes_tests import current_ms, duration_ms


def max_of_nbit(n: int) -> int:
    """
        Integer value from n times '1' in number's binary representation.
    """
    return int('1' * n, 2)


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
    def split(secret: int, n: int, t: int, bit_size: int = 512) -> ([int], int):
        while (p := random_prime(bit_size)) <= secret and p <= n: pass

        p = 1523
        a = [62, 352]
        #a = [randint_bits(bit_size) for _ in range(t - 1)]

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
        total, products = 0, []

        for xj, yj in s:

            prod = 1
            for xi, yi in s:
                if xi != xj:
                    prod *= xi / (xi - xj)

            prod *= yj
            total += prod

        return int(round(total, 0))

    @staticmethod
    def test():
        pass


if __name__ == '__main__':
    # Trivial.test()
    # Schamir.test()

    secret = 954

    split, p = Schamir.split(secret, 4, 3)
    print(f"{split=}")

    merged = Schamir.merge([(2, 383), (3, 1045), (4, 308)], 1523)
    print(f"{merged=}")

    assert secret == merged
