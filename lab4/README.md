## Execution time tests

```
KEY = LHZAPODHYQESOCCP

Testing with a file of 1MB...
ECB...
e=2, d=6	total = 8 [ms]
CBC...
e=4, d=8	total = 12 [ms]
OFB...
e=4, d=9	total = 13 [ms]
CFB...
e=38, d=42	total = 80 [ms]
CTR...
e=2, d=6	total = 8 [ms]

Testing with a file of 200MB...
ECB...
e=429, d=1316	total = 1745 [ms]
CBC...
e=921, d=1653	total = 2574 [ms]
OFB...
e=820, d=1744	total = 2564 [ms]
CFB...
e=7597, d=8188	total = 15785 [ms]
CTR...
e=395, d=1280	total = 1675 [ms]

Testing with a file of 500MB...
ECB...
e=1133, d=3401	total = 4534 [ms]
CBC...
e=2338, d=4126	total = 6464 [ms]
OFB...
e=2061, d=4266	total = 6327 [ms]
CFB...
e=18971, d=20537	total = 39508 [ms]
CTR...
e=988, d=3189	total = 4177 [ms]
```

## Byte corruption tests

```
Plain text = "some text to check how will the output look after the ciphertext is corrupted"
Key = "PRJKCXLQTEYFWMDG"

ECB...
byte 1 = b'\\\x85\xb8\x18 \xfa\xbf\x03\x1f\xee\xa6\x93\x9e#E\xf5ck how will the output look after the ciphertext is corrupted'
byte 24 = b'some text to che\xd0\xb7\xa8M\xaa\x96\xff\xa3\xb9n\x86\xe2WA\xf7joutput look after the ciphertext is corrupted'
byte 48 = b'some text to check how will the ~\xee\\d\xd9Fa\xf2\x90y\xee\xce\xb7g\x11\xd6r the ciphertext is corrupted'
byte 72 = b'some text to check how will the output look afte\\\xb6\x90\xfd\xb9d\x1d0\xcc\x16A\x944!8; is corrupted'
CBC...
byte 1 = b'9B\xec\xd7;5\xd2\xe1+\x92\xa3\xa1\x88\xffc\x18c{ how will the output look after the ciphertext is corrupted\x03\x03\x03'
byte 20 = b'/\xd9(\xb8\x1b\xbaW]&h\xd6P\xf0\xba\x8bKck how will the$output look after the ciphertext is corrupted\x03\x03\x03'
byte 40 = b'some text to che\xf5l\x8b\xbb\xef\x1f$\xdc\xaf\xa8\xdb|\xd5\xc3\xbc\xbboutput look afper the ciphertext is corrupted\x03\x03\x03'
byte 60 = b"some text to check how will the Q\xe8,\x08\xa6\x92\x00K\xf2\x8b'\x07(\xf0\x97Rr the ciphertIxt is corrupted\x03\x03\x03"
byte 79 = b'some text to check how will the output look afte\x8f\x13\x0f\xa3#\xd2\xd5\xdd\xd9E\x90\xe7\xa9\xde\x1b\xb3 is corruptdd\x03\x03\x03'
OFB...
byte 19 = b'some text to ckeck how will the output look after the ciphertext is corrupted'
byte 38 = b'some text to check how will u\xa8e output look after the ciphertext is corrupted'
byte 57 = b'some text to check how will the output look\xd0after the ciphertext is corrupted'
byte 76 = b'some text to check how will the output look after the cipdertext is corrupted'
CFB...
byte 1 = b's\x1f#-X\xc7\x9fHF\xa2\xe1\x88\xde\xf4\xd8\xa6o\xaa how will the output look after the ciphertext is corrupted'
byte 19 = b'some text to ck>U\xf8u\xec\xf5\xe3\x1a\xc4LS.\x83FK\x81 output look after the ciphertext is corrupted'
byte 38 = b'some text to check how will t(\xc2M\x048\xfa\x17\xe5E\x0f\xcc\x97\x11XsN\xf3ter the ciphertext is corrupted'
byte 57 = b'some text to check how will the output look0\x1dm\x83@S\xfbb)\xad\xdem\xe0$#[wtext is corrupted'
byte 76 = b'some text to check how will the output look after the ciplt\r\x1d^(\xa0\xe6i\xc2?\x06\x0f\x14\x83\xa6\xd4ted'
CTR...
byte 1 = b's_me text to check how will the output look after the ciphertext is corrupted'
byte 19 = b'some text to cieck how will the output look after the ciphertext is corrupted'
byte 38 = b'some text to check how will t(e output look after the ciphertext is corrupted'
byte 57 = b'some text to check how will the output look0after the ciphertext is corrupted'
byte 76 = b'some text to check how will the output look after the cipdertext is corrupted'
```
