# crypto stuff

import os

class Crypto():

    def __init__(self):
        self.p = 23 # big prime
        self.g = 11 # big prime
        self.my_secret = None       # A (if I am A)
        self.shared_secret = None   # our master key
        self.nonce = None
        self.id = None
        self.key = None


    """
    FUNCTION
    what to send to the other party
    """
    def to_send(self):
        return None



    def received(self):
        return None



    def compute_shared_secret(self):
        return 0


    """
    FUNCTION
    Generate nonce from 2^32 values
    Return nonce
    """
    def generate_nonce(self):
        self.nonce = os.urandom(8)
        self.nonce = 9999999
        return self.nonce