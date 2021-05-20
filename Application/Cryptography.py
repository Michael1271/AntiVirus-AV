from Secret_Variables import Cryptography_Key
import hashlib

# A program that deals with Cryptography- encryption and decryption
__author__ = 'Michael Khoshahang'

CHARS = [c for c in (chr(i) for i in range(32, 127))]


def transform(text, key=Cryptography_Key, to_be_decrypted=False):
    """
    The Function transforms the supplied text and returns the result.
    :param text: The text to transform.
    :param key: The key with which to apply the transformation.
    :param to_be_decrypted: Whether to encrypt (False) or decrypt (True).
    :return: the result if the transformation.
    :rtype: str
    """
    result = ''
    for i, c in enumerate(text):
        if c not in CHARS:
            result += c
        else:
            text_index = CHARS.index(c)
            key_index = CHARS.index(key[i % len(key)])
            if to_be_decrypted:
                key_index *= -1
            result += CHARS[(text_index + key_index) % len(CHARS)]
    return result


def encrypt(text, key=Cryptography_Key):
    """
    The function encrypts the given text and returns the result.
    :param text: The text to encrypt.
    :param key: The key with which to perform the encryption.
    :return: the encrypted text
    :rtype: str
    """
    return transform(text, key)


def decrypt(text, key=Cryptography_Key):
    """
    The function decrypts the supplied text and returns the result.
    :param text: The text to be decrypted.
    :param key: The key with which to perform the decryption.
    :return: the decrypted cipher
    :rtype: str
    """
    return transform(text, key, True)


def encrypt_to_hash(text):
    """
    The function gets a text and returns it's hash encryption.
    :param text: the plain text to be encoded
    :return: the hash encryption of the given text
    :rtype: str
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()
