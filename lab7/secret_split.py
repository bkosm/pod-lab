from Cryptodome.Random.random import randint
from Cryptodome.Util.number import getRandomInteger as randint_bits

from lab4.aes_tests import current_ms, duration_ms


class Trivial:
    @staticmethod
    def split(secret: int, k: int, n: int) -> [int]:
        s = [randint(0, k - 1) for _ in range(n - 1)]
        sn = (secret + sum([-e for e in s])) % k

        return s + [sn]

    @staticmethod
    def merge(s: [int], k: int): return sum(s) % k

    @staticmethod
    def test() -> None:
        secret = randint_bits(128)
        k = int('1' * 128, 2)
        n = randint(10, 100)

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
    def split():
        pass

    @staticmethod
    def merge():
        pass

    @staticmethod
    def test():
        pass


if __name__ == '__main__':
    Trivial.test()
    Schamir.test()
