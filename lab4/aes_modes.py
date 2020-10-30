from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding


def to_paded_bytes(raw: str, block_size: int = 32) -> bytes:
    return Padding.pad(bytes(raw, 'utf8'), block_size)


def unpad(raw: bytes, block_size: int = 32) -> bytes:
    return Padding.unpad(raw, block_size)


class ECB:
    @staticmethod
    def encrypt(raw: str, key: str) -> bytes:
        """
        AES ECB encryption using Pycryptodome
        :param raw: string to encrypt
        :param key: key as string
        :return: encrypted message as bytes
        """
        data_bytes = to_paded_bytes(raw)
        key_bytes = key.encode('utf8')

        cipher = AES.new(key_bytes, AES.MODE_ECB)
        return cipher.encrypt(data_bytes)

    @staticmethod
    def decrypt(ciphertext: bytes, key: str) -> str:
        """
        AES ECB decryption using Pycryptodome
        :param ciphertext: bytes of the ciphertext
        :param key: key as string
        :return: decrypted message as string
        """
        key_bytes = key.encode('utf8')

        decrypter = AES.new(key_bytes, AES.MODE_ECB)
        result = decrypter.decrypt(ciphertext)

        return str(unpad(result))


class CBC:
    @staticmethod
    def encrypt(raw: str, key: str) -> (bytes, bytes):
        """
        AES CBC encryption using Pycryptodome
        :param raw: string to encrypt
        :param key: key as string
        :return: encrypted message as bytes and iv of the cipher
        """
        data_bytes = to_paded_bytes(raw, 16)
        key_bytes = key.encode('utf8')

        cipher = AES.new(key_bytes, AES.MODE_CBC)
        return cipher.encrypt(data_bytes), cipher.iv

    @staticmethod
    def decrypt(ciphertext: bytes, iv: bytes, key: str) -> str:
        """
        AES CBC decryption using Pycryptodome
        :param ciphertext: bytes of the ciphertext
        :param iv: bytes of the initialization vector used by the cipher
        :param key: key as string
        :return: decrypted message as string
        """
        key_bytes = key.encode('utf8')

        decrypter = AES.new(key_bytes, AES.MODE_CBC, iv=iv)
        return str(decrypter.decrypt(ciphertext))


class OFB:
    @staticmethod
    def encrypt(raw: str, key: str) -> (bytes, bytes):
        """
        AES OFB encryption using Pycryptodome
        :param raw: string to encrypt
        :param key: key as string
        :return: encrypted message as bytes and iv of the cipher
        """
        data_bytes = raw.encode('utf8')
        key_bytes = key.encode('utf8')

        cipher = AES.new(key_bytes, AES.MODE_OFB)
        return cipher.encrypt(data_bytes), cipher.iv

    @staticmethod
    def decrypt(ciphertext: bytes, iv: bytes, key: str) -> str:
        """
        AES OFB decryption using Pycryptodome
        :param ciphertext: bytes of the ciphertext
        :param iv: bytes of the initialization vector used by the cipher
        :param key: key as string
        :return: decrypted message as string
        """
        key_bytes = key.encode('utf8')

        decrypter = AES.new(key_bytes, AES.MODE_OFB, iv=iv)
        return str(decrypter.decrypt(ciphertext))


class CFB:
    @staticmethod
    def encrypt(raw: str, key: str) -> (bytes, bytes):
        """
        AES CFB encryption using Pycryptodome
        :param raw: string to encrypt
        :param key: key as string
        :return: encrypted message as bytes and iv of the cipher
        """
        data_bytes = raw.encode('utf8')
        key_bytes = key.encode('utf8')

        cipher = AES.new(key_bytes, AES.MODE_CFB)
        return cipher.encrypt(data_bytes), cipher.iv

    @staticmethod
    def decrypt(ciphertext: bytes, iv: bytes, key: str) -> str:
        """
        AES CFB decryption using Pycryptodome
        :param ciphertext: bytes of the ciphertext
        :param iv: bytes of the initialization vector used by the cipher
        :param key: key as string
        :return: decrypted message as string
        """
        key_bytes = key.encode('utf8')

        decrypter = AES.new(key_bytes, AES.MODE_CFB, iv=iv)
        return str(decrypter.decrypt(ciphertext))


class CTR:
    @staticmethod
    def encrypt(raw: str, key: str) -> (bytes, bytes):
        """
        AES CTR encryption using Pycryptodome
        :param raw: string to encrypt
        :param key: key as string
        :return: encrypted message as bytes and nonce of the cipher
        """
        data_bytes = raw.encode('utf8')
        key_bytes = key.encode('utf8')

        cipher = AES.new(key_bytes, AES.MODE_CTR)
        return cipher.encrypt(data_bytes), cipher.nonce

    @staticmethod
    def decrypt(ciphertext: bytes, nonce: bytes, key: str) -> str:
        """
        AES CTR decryption using Pycryptodome
        :param ciphertext: bytes of the ciphertext
        :param nonce: bytes of the nonce used by the cipher
        :param key: key as string
        :return: decrypted message as string
        """
        key_bytes = key.encode('utf8')

        decrypter = AES.new(key_bytes, AES.MODE_CTR, nonce=nonce)
        return str(decrypter.decrypt(ciphertext))
