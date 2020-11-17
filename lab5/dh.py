from math import sqrt
from typing import Union

from Cryptodome.Random.random import getrandbits

from lab3.bbs import BBS
from lab4.aes_tests import current_ms, duration_ms


class DiffiHelman:
    random_prime = BBS.random_prime

    @staticmethod
    def find_coprimes(modulo: int) -> set[int]:
        out = set()

        while modulo % 2 == 0:
            out.add(2)
            modulo //= 2

        for i in range(3, int(sqrt(modulo)), 2):
            while modulo % i == 0:
                out.add(i)
                modulo //= i

        if modulo > 2:
            out.add(modulo)

        return out

    @staticmethod
    def first_primitive_root(modulo: int) -> Union[int, None]:
        phi = modulo - 1

        coprimes = DiffiHelman.find_coprimes(phi)

        for r in range(2, phi + 1):
            for it in coprimes:
                if pow(r, phi // it, modulo) != 1:
                    return r

        return None

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

        print(f"n = {prime}, g = {root}")

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

    def generate_public_key(self, private_bit_size: int = 256) -> int:
        self.__private_key, self.public_key = DiffiHelman.intermediate_keys(self.prime, self.root, private_bit_size)

        return self.public_key

    def digest_public_key(self, public_key: int) -> None:
        self.session_key = DiffiHelman.session_key(self.__private_key, public_key, self.prime)


def main() -> None:
    prime, root = DiffiHelman.random_arguments(56)

    print(f"n = {prime}, g = {root}")

    a = Application(prime, root)
    b = Application(prime, root)

    a.generate_public_key()
    b.generate_public_key()

    print(f"a public = {a.public_key}, b public = {b.public_key}")

    a.digest_public_key(b.public_key)
    b.digest_public_key(a.public_key)

    print(f"a key = {a.session_key}, b key = {b.session_key}")


if __name__ == '__main__':
    main()

    print("\nTest:")
    DiffiHelman.test(56)
