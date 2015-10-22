# crypto stuff

import os
from Crypto.Cipher import AES
from Crypto import Random
import base64


class CryptoCore():

    def __init__(self, key, id):
        self.p = 997
        self.g = 191
        self.A = int.from_bytes(Random.get_random_bytes(2), byteorder='little')
        self.shared_secret = None
        self.session_key = self.gen_session_key()
        self.my_nonce = self.generate_nonce()
        self.peer_nonce = None
        self.id = id
        self.key = key
        self.iv = Random.new().read(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)

    """
    FUNCTION
    Generate nonce from 2^32 values
    Return nonce
    """
    def generate_nonce(self):
        self.my_nonce = Random.get_random_bytes(4)
        return self.my_nonce


    """
    FUNCTION
    return g**secret
    """
    def gen_session_key(self):
        return ((self.g ** self.A) % self.p)


    """
    FUNCTION
    Encrypt second message
    """
    def encrypt_all(self):
        plain_text = self.id + " " + self.peer_nonce \
                     + " " + str(self.session_key)

        if(len(plain_text) < 32):
            plain_text = plain_text.zfill(32)
        msg =  base64.b64encode(self.iv + self.cipher.encrypt(plain_text))

        return msg

    """
    FUNCTION
    """
    def decrypt_all(self, ciphertext):
        plaintext = self.cipher.decrypt(base64.b64decode(ciphertext))
        return plaintext
