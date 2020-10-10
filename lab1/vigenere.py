from argparse import *

parser = ArgumentParser(description="Encrypt or decrypt given message with the Vignere cipher.")

mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument('--enc', action='store_true', help='run encryption')
mode_group.add_argument('--dec', action='store_true', help='run decryption')

input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument('-t', metavar='TEXT', help='use inline text')
input_group.add_argument('-f', metavar='FILEPATH', help='use text from file')

parser.add_argument('-k', metavar='KEY', help='encryption key', required=True)

parser.add_argument('-o', metavar='FILEPATH', help='output to file with given path')

args = parser.parse_args()
