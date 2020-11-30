import argparse as argp
from typing import Any, Callable
from Cryptodome.Hash import MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512

from lab4.aes_tests import current_ms, duration_ms

ALGORITHMS = {'md5': MD5.new,
              'sha1': SHA1.new,
              'sha2': {224: SHA224.new,
                       256: SHA256.new,
                       384: SHA384.new,
                       512: SHA512.new},
              'sha3': {224: SHA3_224.new,
                       256: SHA3_256.new,
                       384: SHA3_384.new,
                       512: SHA3_512.new}}


def hexdigest(algorithm: Callable, text: str, encoding='utf8') -> str:
    return algorithm(text.encode(encoding)).hexdigest()


def __get_command_line_args() -> dict[str, Any]:
    sha_variants = {224, 256, 384, 512}

    parser = argp.ArgumentParser(description="hexdigest on given input with specified algorithm")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='message to digest')
    input_group.add_argument('--file', type=str, help='digest given file')

    alg_group = parser.add_mutually_exclusive_group(required=True)
    alg_group.add_argument('--md5', action='store_true', help='use md5')
    alg_group.add_argument('--sha1', action='store_true', help='use sha1')
    alg_group.add_argument('--sha2', type=int, choices=sha_variants,
                           help=f'use specified variant of sha2')
    alg_group.add_argument('--sha3', type=int, choices=sha_variants,
                           help=f'use specified variant of sha3')

    parser.add_argument('-v', action='store_true', help='set verbose output (measured time)')

    return vars(parser.parse_args())


if __name__ == '__main__':
    args = __get_command_line_args()
    text = ""
    duration = 0

    if filename := args['file']:
        with open(filename, 'r') as f:
            text = ''.join(f.readlines())

    else:
        text = args['input']

    if args['md5']:
        start = current_ms()
        print(hexdigest(ALGORITHMS['md5'], text))
        duration = duration_ms(start)

    elif args['sha1']:
        start = current_ms()
        print(hexdigest(ALGORITHMS['sha1'], text))
        duration = duration_ms(start)

    elif variant := args['sha2']:
        start = current_ms()
        print(hexdigest(ALGORITHMS['sha2'][variant], text))
        duration = duration_ms(start)

    elif variant := args['sha3']:
        start = current_ms()
        print(hexdigest(ALGORITHMS['sha3'][variant], text))
        duration = duration_ms(start)

    if args['v']:
        print(f"{duration=} [ms]")
