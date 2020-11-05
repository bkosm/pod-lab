from string import ascii_uppercase as ASCII
from typing import Any
import random
import time
import base64
import argparse

from lab4.aes_modes import ECB, CBC, OFB, CFB, CTR
from lab4.create_files import create_files, file_name


def parse_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser(description="Run AES mode performance tests.")
    parser.add_argument('--fsize', metavar='File sizes', type=int, nargs='+',
                        help='sizes of the files used in tests [MB]', required=False)
    parser.add_argument('--runc', action='store_true', help='run the byte corruption tests', required=False)

    return vars(parser.parse_args())


def current_ms() -> int:
    return round(time.time() * 1000)


def duration_ms(start: int) -> int:
    return current_ms() - start


def ecb_test(text: str, key: str) -> (int, int, int):
    start = current_ms()
    ciphertext = ECB.encrypt(text, key)
    encrypt_duration = duration_ms(start)

    start = current_ms()
    result = ECB.decrypt(ciphertext, key)
    decrypt_duration = duration_ms(start)

    total = encrypt_duration + decrypt_duration

    print(f"e={encrypt_duration}, d={decrypt_duration}\t"
          + f"total = {encrypt_duration + decrypt_duration} [ms]")

    return encrypt_duration, decrypt_duration, total


def cbc_test(text: str, key: str) -> (int, int, int):
    start = current_ms()
    ciphertext, iv = CBC.encrypt(text, key)
    encrypt_duration = duration_ms(start)

    start = current_ms()
    result = CBC.decrypt(ciphertext, iv, key)
    decrypt_duration = duration_ms(start)

    total = encrypt_duration + decrypt_duration

    print(f"e={encrypt_duration}, d={decrypt_duration}\t"
          + f"total = {total} [ms]")

    return encrypt_duration, decrypt_duration, total


def ofb_test(text: str, key: str) -> (int, int, int):
    start = current_ms()
    ciphertext, iv = OFB.encrypt(text, key)
    encrypt_duration = duration_ms(start)

    start = current_ms()
    result = OFB.decrypt(ciphertext, iv, key)
    decrypt_duration = duration_ms(start)

    total = encrypt_duration + decrypt_duration

    print(f"e={encrypt_duration}, d={decrypt_duration}\t"
          + f"total = {total} [ms]")

    return encrypt_duration, decrypt_duration, total


def cfb_test(text: str, key: str) -> (int, int, int):
    start = current_ms()
    ciphertext, iv = CFB.encrypt(text, key)
    encrypt_duration = duration_ms(start)

    start = current_ms()
    result = CFB.decrypt(ciphertext, iv, key)
    decrypt_duration = duration_ms(start)

    total = encrypt_duration + decrypt_duration

    print(f"e={encrypt_duration}, d={decrypt_duration}\t"
          + f"total = {total} [ms]")

    return encrypt_duration, decrypt_duration, total


def ctr_test(text: str, key: str) -> (int, int, int):
    start = current_ms()
    ciphertext, nonce = CTR.encrypt(text, key)
    encrypt_duration = duration_ms(start)

    start = current_ms()
    result = CTR.decrypt(ciphertext, nonce, key)
    decrypt_duration = duration_ms(start)

    total = encrypt_duration + decrypt_duration

    print(f"e={encrypt_duration}, d={decrypt_duration}\t"
          + f"total = {total} [ms]")

    return encrypt_duration, decrypt_duration, total

def get_averages(results: list[tuple[int, int, int]]) -> (int, int, int):
    sum_enc = 0
    sum_dec = 0
    sum_tot = 0

    for (e, d, t) in results:
        sum_enc += e
        sum_dec += d
        sum_tot += t

    return sum_enc / len(results), sum_dec / len(results), sum_tot / len(results)

def file_test(sizes: list[int]) -> None:
    create_files(sizes)
    rounds = 5

    key = ''.join([random.choice(ASCII) for _ in range(16)])
    print(f'KEY = {key}')

    for size in sizes:
        with open(file_name(size), 'r') as f:
            text = ''.join(f.readlines())

            print(f"\nTesting with a file of {size}MB...")

            print(f"ECB...")
            e, d, t = get_averages([ecb_test(text, key) for _ in range(rounds)])
            print(f"avg enc = {e}\t avg dec = {d}\t avg tot = {t}\n")

            print(f"CBC...")
            e, d, t = get_averages([cbc_test(text, key) for _ in range(rounds)])
            print(f"avg enc = {e}\t avg dec = {d}\t avg tot = {t}\n")

            print(f"OFB...")
            e, d, t = get_averages([ofb_test(text, key) for _ in range(rounds)])
            print(f"avg enc = {e}\t avg dec = {d}\t avg tot = {t}\n")

            print(f"CFB...")
            e, d, t = get_averages([cfb_test(text, key) for _ in range(rounds)])
            print(f"avg enc = {e}\t avg dec = {d}\t avg tot = {t}\n")

            print(f"CTR...")
            e, d, t = get_averages([ctr_test(text, key) for _ in range(rounds)])
            print(f"avg enc = {e}\t avg dec = {d}\t avg tot = {t}\n")


def corrupt(b: bytes, position: int = 0) -> bytes:
    text = base64.b64encode(b)
    corrupted = [chr(c + 1) if i == position else chr(c) for (i, c) in enumerate(text)]

    return base64.b64decode(''.join(corrupted))


def error_test() -> None:
    """
    Byte corruption test, run until no exception is thrown for optimal results
    :raises Exception: When corruption set incorrect bytes
    :return:
    """
    key = ''.join([random.choice(ASCII) for _ in range(16)])
    text = 'some text to check how the output will look after the ciphertext is corrupted'

    print(f'\nByte corruption test\nPlain text = "{text}"\nKey = "{key}"\n')

    print("ECB...")
    ciphertext = ECB.encrypt(text, key)
    positions = [1, int(len(ciphertext) / 4), int(len(ciphertext) / 2),
                 int(3 * len(ciphertext) / 4)]

    for p in positions:
        corrupted = corrupt(ciphertext, p)
        print(f'byte {p} = {ECB.decrypt(corrupted, key)}')

    print("CBC...")
    ciphertext, iv = CBC.encrypt(text, key)
    positions = [1, int(len(ciphertext) / 4), int(len(ciphertext) / 2),
                 int(3 * len(ciphertext) / 4), len(ciphertext) - 1]

    for p in positions:
        corrupted = corrupt(ciphertext, p)
        print(f'byte {p} = {CBC.decrypt(corrupted, iv, key)}')

    print("OFB...")
    ciphertext, iv = OFB.encrypt(text, key)
    positions = [int(len(ciphertext) / 4), int(len(ciphertext) / 2),
                 int(3 * len(ciphertext) / 4), len(ciphertext) - 1]

    for p in positions:
        corrupted = corrupt(ciphertext, p)
        print(f'byte {p} = {OFB.decrypt(corrupted, iv, key)}')

    print("CFB...")
    ciphertext, iv = CFB.encrypt(text, key)
    positions = [1, int(len(ciphertext) / 4), int(len(ciphertext) / 2),
                 int(3 * len(ciphertext) / 4), len(ciphertext) - 1]

    for p in positions:
        corrupted = corrupt(ciphertext, p)
        print(f'byte {p} = {CFB.decrypt(corrupted, iv, key)}')

    print("CTR...")
    ciphertext, nonce = CTR.encrypt(text, key)
    positions = [1, int(len(ciphertext) / 4), int(len(ciphertext) / 2),
                 int(3 * len(ciphertext) / 4), len(ciphertext) - 1]

    for p in positions:
        corrupted = corrupt(ciphertext, p)
        print(f'byte {p} = {CTR.decrypt(corrupted, nonce, key)}')


if __name__ == '__main__':
    args = parse_args()

    if sizes := args['fsize']:
        file_test(sizes)

    if args['runc']:
        error_test()
