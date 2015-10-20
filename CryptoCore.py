# crypto stuff

import os
from Crypto.Cipher import AES
from Crypto import Random


class CryptoCore():

    def __init__(self):
        self.p = 23                                  # big prime
        self.g = 11                                  # big prime
        self.A = int.from_bytes(Random.get_random_bytes(2), byteorder='little')
        self.shared_secret = None   # our master key
        self.session_key = self.gen_session_key()
        self.my_nonce = self.generate_nonce()
        self.peer_nonce = None
        self.id = None
        self.key = None
        self.iv = None


    """
    FUNCTION
    what to send to the other party
    """
    def send_challenge(self):

        return None



    def get_challenge(self):
        return None



    def compute_shared_secret(self):
        return 0


    """
    FUNCTION
    Generate nonce from 2^32 values
    Return nonce
    """
    def generate_nonce(self):
        print("generate noncce function")
        self.my_nonce = Random.get_random_bytes(4)
        #self.my_nonce = 9999999
        return self.my_nonce


    """
    FUNCTION
    return g**secret % p
    """
    def gen_session_key(self):
        print("in gen session key; A %d, g %d, p %d" %
              (self.A, self.g, self.p))

        return ((self.g ** self.A) % self.p)


    """
    FUNCTION
    Encrypt second message
    """
    def encrypt_all(self):
        plain_text = self.id + " " + self.peer_nonce \
                     + " " + self.session_key
        self.iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        msg = self.iv + cipher.encrypt(plain_text)
        print("msg is %s" % msg)
        return msg