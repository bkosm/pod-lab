import argparse as argp
import re
import string


def get_args() -> argp.Namespace:
    parser = argp.ArgumentParser(description="Encrypt or decrypt given message with the Vignere cipher.")

    parser.add_argument('-v', action='store_true', help='set verbose output')
    parser.add_argument('--dec', action='store_true', help='run decryption instead of encryption')

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-t', type=str, metavar='TEXT', help='use inline text')
    input_group.add_argument('-f', type=str, metavar='FILEPATH', help='use text from file')

    parser.add_argument('-k', type=str, metavar='KEY', help='encryption key', required=True)
    parser.add_argument('-o', type=str, metavar='FILEPATH', help='output to file with given path')
    parser.add_argument('--alphabet', type=str, metavar='STRING', help='use a custom alphabet indexed in given order '
                                                                       '(ex. "ABCD_")')

    return parser.parse_args()


class Vigenere:
    def __init__(self, alphabet=(string.ascii_uppercase + '_')):
        self.ALPHABET = alphabet
        self.CHAR_MAP = dict(zip([c for c in self.ALPHABET], [i for i in range(0, len(self.ALPHABET))]))

        self.matrix = [[] for _ in range(3)]

    def print_setup(self):
        print(f'Alphabet: {self.ALPHABET}')
        print(f'Text:     {self.matrix[0]}')
        print(f'Key fill: {self.matrix[1]}')
        print(f'Cipher:   {self.matrix[2]}\n')

    def encrypt(self, text: str, key: str) -> str:
        self._verify_input_text(text)
        self._verify_input_text(key)

        self.matrix = [[c for c in text]]

        text_len = len(self.matrix[0])

        key_fill = [key[i % len(key)] for i in range(text_len)]

        self.matrix += [key_fill]
        self.matrix += [[' ' for _ in range(text_len)]]

        for i in range(len(self.matrix[0])):
            char_index = (self.CHAR_MAP[self.matrix[0][i]] + self.CHAR_MAP[self.matrix[1][i]]) % len(self.ALPHABET)

            self.matrix[2][i] = next((key for (key, value) in self.CHAR_MAP.items() if value == char_index))

        return ''.join(self.matrix[2])

    def decrypt(self, text: str, key: str) -> str:
        self._verify_input_text(text)
        self._verify_input_text(key)

        self.matrix = [[c for c in text]]

        text_len = len(self.matrix[0])

        key_fill = [key[i % len(key)] for i in range(text_len)]

        self.matrix = [key_fill] + self.matrix
        self.matrix = [[' ' for _ in range(text_len)]] + self.matrix

        for i in range(len(self.matrix[0])):
            char_index = self.CHAR_MAP[self.matrix[2][i]] - self.CHAR_MAP[self.matrix[1][i]]

            if char_index < 0:
                char_index += len(self.ALPHABET)

            self.matrix[0][i] = next((key for (key, value) in self.CHAR_MAP.items() if value == char_index))

        return ''.join(self.matrix[0])

    def _verify_input_text(self, text: str) -> None:
        for letter in text:
            assert letter in self.ALPHABET, "a letter in the input text doesn't match the alphabet"


if __name__ == '__main__':
    ARGS = vars(get_args())

    app = Vigenere()

    text = ''

    if text := ARGS['t']:
        pass

    elif filepath := ARGS['f']:
        with open(filepath, 'r') as f:
            text = ''.join(f.readlines())

    text = re.sub(r'[\t\r\n ]', '', text).upper()
    key = re.sub(r'[\t\r\n ]', '', ARGS['k']).upper()

    if ARGS['dec']:
        text = app.decrypt(text, key)

    else:
        text = app.encrypt(text, key)

    if ARGS['v']:
        app.print_setup()

    if filepath := ARGS['o']:
        with open(filepath, 'w') as f:
            f.write(text)

    else:
        print(text)
