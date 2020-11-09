from math import gcd
from Cryptodome.Random.random import getrandbits

from lab3.bbs import Bbs
from lab4.aes_tests import current_ms, duration_ms


class DiffiHelman:
    random_prime = Bbs.random_prime

    @staticmethod
    def first_primitive_root(modulo: int) -> int:
        coprimes = {num for num in range(1, modulo) if gcd(num, modulo) == 1}

        return next(g for g in range(1, modulo) if coprimes == {pow(g, powers, modulo)
                                                                for powers in range(1, modulo)})

    @staticmethod
    def random_arguments(prime_bit_size: int = 16) -> (int, int):
        prime = DiffiHelman.random_prime(prime_bit_size)

        return prime, DiffiHelman.first_primitive_root(prime)

    @staticmethod
    def intermediate_keys(prime: int, root: int, bit_size: int = 256) -> (int, int):
        rand = getrandbits(bit_size)

        return rand, pow(root, rand, prime)

    @staticmethod
    def session_key(private: int, public: int, prime: int) -> int:
        return pow(public, private, prime)

    @staticmethod
    def test(prime_bit_size: int = 20) -> None:
        start = current_ms()
        prime, root = DiffiHelman.random_arguments(prime_bit_size)
        print(f"'n' and 'g' generation time = {duration_ms(start)} [ms]")

        start = current_ms()
        a_priv, a_public = DiffiHelman.intermediate_keys(prime, root)
        print(f"intermediate key generation time = {duration_ms(start)} [ms]")

        b_priv, b_public = DiffiHelman.intermediate_keys(prime, root)

        start = current_ms()
        a_key = DiffiHelman.session_key(a_priv, b_public, prime)
        print(f"session key generation time = {duration_ms(start)} [ms]")

        b_key = DiffiHelman.session_key(b_priv, a_public, prime)

        assert a_key == b_key, "keys differ"


class Application:
    def __init__(self, prime: int, root: int):
        self.prime = prime
        self.root = root

        self.__private_key, self.public_key, self.session_key = 0, 0, 0

    def generate_public_key(self, private_bit_size: int = 256):
        self.__private_key, self.public_key = DiffiHelman.intermediate_keys(self.prime, self.root, private_bit_size)

        return self.public_key

    def digest_public_key(self, public_key: int) -> None:
        self.session_key = DiffiHelman.session_key(self.__private_key, public_key, self.prime)


if __name__ == '__main__':
    prime, root = DiffiHelman.random_arguments(20)

    a = Application(prime, root)
    b = Application(prime, root)

    a.generate_public_key()
    b.generate_public_key()

    print(f"a public = {a.public_key}, b public = {b.public_key}")

    a.digest_public_key(b.public_key)
    b.digest_public_key(a.public_key)

    print(f"a key = {a.session_key}, b key = {b.session_key}")
