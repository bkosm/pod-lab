import argparse as argp
import re
import string
from typing import Any


class Vigenere:
    def __init__(self, alphabet=(string.ascii_uppercase + '_ .,-:')):
        """
        Construct the Vigenere cipher solver object.

        :param alphabet: Custom alphabet to use, the default is [A-Z_ .,-:].
        """
        self.__char_map: dict[str, int] = None
        self.__matrix: list[list] = [[] for _ in range(3)]

        self.alphabet: str = alphabet

    @property
    def alphabet(self) -> str:
        return self.__alphabet

    @alphabet.setter
    def alphabet(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError("the given alphabet must be str")

        self.__alphabet = value
        self.__char_map = dict(zip([c for c in self.__alphabet], [i for i in range(0, len(self.__alphabet))]))

    def print_setup(self) -> None:
        """
        Print used alphabet, decrypted text, key setup and the cipher.
        """
        print(f'Alphabet: {self.alphabet}')
        print(f'Text:     {self.__matrix[0]}')
        print(f'Key fill: {self.__matrix[1]}')
        print(f'Cipher:   {self.__matrix[2]}\n')

    def encrypt(self, text: str, key: str) -> str:
        self.__verify_input(text)
        self.__verify_input(key)

        text_fill = [c for c in text]
        key_fill = [key[i % len(key)] for i in range(len(text))]
        cipher_fill = [' ' for _ in range(len(text))]

        self.__matrix = [text_fill] + [key_fill] + [cipher_fill]

        for i in range(len(text)):
            char_index = (self.__char_map[self.__matrix[0][i]] + self.__char_map[self.__matrix[1][i]]) % len(
                self.alphabet)

            self.__matrix[2][i] = next((key for (key, value) in self.__char_map.items() if value == char_index))

        return ''.join(self.__matrix[2])

    def decrypt(self, text: str, key: str) -> str:
        self.__verify_input(text)
        self.__verify_input(key)

        text_fill = [' ' for _ in range(len(text))]
        key_fill = [key[i % len(key)] for i in range(len(text))]
        cipher_fill = [c for c in text]

        self.__matrix = [text_fill] + [key_fill] + [cipher_fill]

        for i in range(len(self.__matrix[0])):
            char_index = self.__char_map[self.__matrix[2][i]] - self.__char_map[self.__matrix[1][i]]

            if char_index < 0:
                char_index += len(self.alphabet)

            self.__matrix[0][i] = next((key for (key, value) in self.__char_map.items() if value == char_index))

        return ''.join(self.__matrix[0])

    def __verify_input(self, text: str) -> None:
        """
        Check whether the text contains valid chars.

        :raises ValueError: When any char in given text doesn't exist in the object's alphabet.
        """
        for letter in text:
            if (l := letter) not in self.alphabet:
                raise ValueError(f"a letter in the input text doesn't match the alphabet -> {l}")

    @staticmethod
    def prepare_string(text: str) -> str:
        """
        Clean string from tabs, carriage returns and line feeds and set it to uppercase.
        """
        return re.sub(r'[\t\r\n]', '', text).upper()


class ConsoleApplication:
    @staticmethod
    def __get_command_line_args() -> dict[str, Any]:
        """
        Parse command line arguments used by the Vigenere solver object and return them as a dictionary.
        """
        parser = argp.ArgumentParser(description="Encrypt or decrypt given message with the Vignere cipher.")

        parser.add_argument('-v', action='store_true', help='set verbose output')
        parser.add_argument('--dec', action='store_true', help='run decryption instead of encryption')

        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument('-t', type=str, metavar='TEXT', help='use inline text')
        input_group.add_argument('-f', type=str, metavar='FILEPATH', help='use text from file')

        parser.add_argument('-k', type=str, metavar='KEY', help='encryption key', required=True)
        parser.add_argument('-o', type=str, metavar='FILEPATH', help='output to file with given path')
        parser.add_argument('--alphabet', type=str, metavar='STRING',
                            help='use a custom alphabet indexed in given order '
                                 '(ex. "ABCD_")')

        return vars(parser.parse_args())

    @staticmethod
    def run() -> None:
        """
        Run the Vigenere solver as a console application.
        """
        app = Vigenere()
        args = ConsoleApplication.__get_command_line_args()

        if alphabet := args['alphabet']:
            app.alphabet = alphabet

        if text := args['t']:
            pass
        elif filepath := args['f']:
            with open(filepath, 'r') as f:
                text = ''.join(f.readlines())

        text = Vigenere.prepare_string(text)
        key = Vigenere.prepare_string(args['k'])

        assert app and text and key, "one of the main objects haven't been initialized"

        if args['dec']:
            text = app.decrypt(text, key)
        else:
            text = app.encrypt(text, key)

        if args['v']:
            app.print_setup()

        if filepath := args['o']:
            with open(filepath, 'w') as f:
                f.write(text)
        else:
            print(text)


if __name__ == '__main__':
    ConsoleApplication.run()
