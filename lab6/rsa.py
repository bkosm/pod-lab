from math import gcd

from Cryptodome.Util.number import getPrime as random_prime


def are_coprimes(prime_a: int, prime_b: int) -> bool:
    return gcd(prime_a, prime_b) == 1


def extended_gcd(a: int, b: int) -> (int, int, int):
    if a == 0:
        return b, 0, 1

    gcd, a_div_gcd, b_div_gcd = extended_gcd(b % a, a)
    return gcd, b_div_gcd - (b // a) * a_div_gcd, a_div_gcd


class RSA:
    @staticmethod
    def find_random_e(phi, bit_size=64):
        e = random_prime(bit_size)

        while not are_coprimes(phi, e):
            e = random_prime(bit_size)

        return e

    @staticmethod
    def find_d(phi, e):
        g, x, y = extended_gcd(e, phi)

        return x % phi if g == 1 else None

    @staticmethod
    def generate_keys() -> ((int, int), (int, int)):
        p = random_prime(256)
        q = random_prime(256)

        n = p * q

        phi = (p - 1) * (q - 1)

        e = RSA.find_random_e(phi, 512)

        d = RSA.find_d(phi, e)

        print(f"{p=} {q=} {n=} {phi=} {e=} {d=}")

        return (e, n), (d, n)

    @staticmethod
    def encrypt(message: str, keys: (int, int)) -> [int]:
        e, n = keys

        return [pow(ord(c), e, n) for c in message]

    @staticmethod
    def decrypt(encrypted: [int], keys: (int, int)) -> str:
        d, n = keys

        return ''.join([chr(pow(c, d, n)) for c in encrypted])


if __name__ == '__main__':
    public, private = RSA.generate_keys()
    text = "Typowy testowy tekst z polskim znakiem ń."

    encrypted = RSA.encrypt(text, public)

    print(f"{encrypted=}")

    decrypted = RSA.decrypt(encrypted, private)

    print(f"{decrypted=}")

