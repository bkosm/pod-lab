# pod-lab

Quick guide:
* `lab2` - Vigenere cipher console application
* `lab3` - BBS random bit generator and a couple of Fips tests
* `lab4` - AES modes available from `PyCryptoDome` with execution time tests for various filesizes 
* `lab5` - Implementation of Diffi-Helman key generation algorithm 
* `lab6` - Implementation of the RSA cipher
* `lab7` - Implementation of secret splitting - Trivial, Schamir modulo prime (needs work) and simple Schamir algorithms
* `lab8` - Hashing utility console application


To use the scripts directly from the command line specify the parent package:

```shell script
# running hashing utility script

python -m lab8.hash_util .\lab8\hash_util.py
```

The `-m` is due to relative imports.

> Podstawy Ochrony Danych, semestr 5 @ PUT