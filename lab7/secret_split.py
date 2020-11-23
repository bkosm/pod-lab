from Cryptodome.Random.random import randint as randint_range
from Cryptodome.Util.number import getRandomInteger as randint_bits, getPrime as random_prime

from random import sample

from lab4.aes_tests import current_ms, duration_ms


def max_of_nbit(n: int) -> int:
    """ Integer value from n times '1' in number's binary representation.
    """
    return int('1' * n, 2)


def neg_mod(num: int, value: int) -> int:
    """ Negative modulus to standard format.
        Example: `neg_mod(-5, 4) == 1`
    """
    return num - int(num / value) * value


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
    def split(secret: int, n: int, t: int, p: int = None, bit_size: int = 16) -> ([int], int):
        if not p:
            while (p := random_prime(bit_size)) <= secret and p <= n: pass

        a = [randint_bits(bit_size) for _ in range(t - 1)]

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

        for i, si in s:
            top = 1
            bottom = 1

            for x, _ in s:
                if i == x: continue

                top *= -x
                bottom *= (i - x)

            if neg_mod(top, bottom) == 0:
                value = top / bottom

            else:
                value = 1
                while value * bottom % p != top:
                    value += 1

            factors.append(int(neg_mod(value * si, p)))

        return sum(factors)

    @staticmethod
    def test():
        secret = 1000
        n = 4
        t = 3

        split, p = Schamir.split(secret, n, t)
        print(f"{split=}")
        print(f"{p=}")

        pool = sample(split, t)
        print(f"{pool=}")

        merged = Schamir.merge(pool, p)
        print(f"{merged=}")

        assert secret == merged


if __name__ == '__main__':
    # Trivial.test()
    Schamir.test()
