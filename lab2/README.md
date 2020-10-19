```
usage: vigenere.py [-h] [-v] [--dec] (-t TEXT | -f FILEPATH) -k KEY [-o FILEPATH] [--alphabet STRING]

Encrypt or decrypt given message with the Vignere cipher.

optional arguments:
  -h, --help         show this help message and exit
  -v                 set verbose output
  --dec              run decryption instead of encryption
  -t TEXT            use inline text
  -f FILEPATH        use text from file
  -k KEY             encryption key
  -o FILEPATH        output to file with given path
  --alphabet STRING  use a custom alphabet indexed in given order (ex. "ABCD_")
```