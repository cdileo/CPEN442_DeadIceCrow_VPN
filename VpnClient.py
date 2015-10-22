import threading
import socket
import select
import sys
from Parser import Parser
from enum import Enum
import struct

# Constants
BUFFER_SIZE = 4096


class State(Enum):
    Init = 0
    KeyX = 1
    Challenge = 2
    Final = 3


class VpnClient(threading.Thread):

    def __init__(self, server, port, crypto):
        self.server = server
        self.port = port
        self.socket_list = []
        self.my_socket = None
        self.crypto = crypto
        self.state = State.Init
        self.destructCount = 10

    """
    FUNCTION
     starts client application of the VPN
    """
    def start_client(self):
        print("start_client: starting client")
        # create socket to connect
        self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mysocket.settimeout(2)

        # connect to remote host
        try:
            self.mysocket.connect((self.server, self.port))
        except:
            print ('Unable to connect: check provided host name, port and make sure server is up')
            return 1

        print("Connection established")
        sys.stdout.write("[Me] ")
        sys.stdout.flush()



        # Enter loop and alternate reading from stdin and socket
        while 1:
            self.socket_list = [sys.stdin, self.mysocket]

            # Get readable sockets with select()
            ready_to_read, ready_to_write, in_error = select.select(self.socket_list, [], [])

            for sock in ready_to_read:
                if sock == self.mysocket:
                    # if this is our socket then read from it
                    if self.state != State.Final:
                        while self.state != State.Final:

                            if self.state == State.Init:
                                print("P is "+str(self.crypto.p))
                                print("G is "+str(self.crypto.g))

                                data = sock.recv(BUFFER_SIZE)
                                # If you can't read - connection interruption - exit
                                if not data:
                                    print ('\nDisconnected from chat server')
                                    sys.exit()
                                else:
                                    parser = Parser()
                                    response = parser.parse_data(data)
                                    self.crypto.peer_nonce = response[0]
                                    print("PEER NONCE")
                                    print(self.crypto.peer_nonce)
                                    self.crypto.id = response[1]

                                    if self.crypto.peer_nonce:
                                        self.state = State.KeyX
                                    else:
                                        print("[ERROR] Did not get a challenge.")
                                        sys.exit(1)

                            elif self.state == State.KeyX:

                                send_data = self.send_challenge_response()
                                sock.send(send_data.encode())

                                ready_to_read, ready_to_write, in_error = select.select(self.socket_list, [], [])
                                for sock2 in ready_to_read:
                                    if sock2 == self.mysocket:
                                        data = sock2.recv(BUFFER_SIZE)


                                if not data:
                                    print("!!!!!!!NO DATA")
                                    sys.exit()

                                self.state = State.Challenge

                            elif self.state == State.Challenge:
                                parser = Parser()

                                response = parser.parse_data(data)

                                parsed_byte_string = parser.parse_response(response[0])

                                plain_txt = self.crypto.decrypt_all(parsed_byte_string.encode())

                                sessionInfo = parser.parse_plaintxt(plain_txt)
                                
                                if int(sessionInfo[1]) != struct.unpack("<L",self.crypto.my_nonce)[0]:
                                    print("[ERROR] Not my nonce, man.")
                                    sys.exit(1)
                                else:
                                    print("verified nonce!")
                                    self.crypto.session_key = (int(sessionInfo[2])**self.crypto.A) % self.crypto.p
                                    self.state = State.Final

                            else:
                                print("BREAK")
                                #break

                    else:
                        # only when the state if FInal
                        data = sock.recv(BUFFER_SIZE)
                        if not data:
                            sys.exit(1)
                        sys.stdout.write(str(sock.getpeername()))
                        sys.stdout.write(": ")
                        decrypted_msg = self.crypto.cipher.decrypt(data)
                        print("received cipher text ", data)
                        sys.stdout.write(decrypted_msg[-32:].decode())
                        sys.stdout.write('[Me] ')
                        sys.stdout.flush()
                        if self.destructCount > 0:
                                self.destructCount -= 1
                        else:
                            print ("Hit our maximum number of messages. Terminating to protect forward secrecy.")
                            print ("Have a nice day :)")
                            sys.exit(0)

                else:
                    if self.destructCount > 0:
                        self.destructCount -= 1
                    else:
                        print ("Hit our maximum number of messages. Terminating to protect forward secrecy.")
                        print ("Have a nice day :)")
                        sys.exit(0)

                    # Read and send user's message
                    msg = sys.stdin.readline()
                    encrypted_msg = self.crypto.cipher.encrypt(msg)
                    print("encrypted message to be sent ", encrypted_msg)
                    self.mysocket.send(encrypted_msg)
                    sys.stdout.write("[Me] ")
                    sys.stdout.flush()


    """
    FUNCTION
     Returns socket object instance
    """
    def get_my_socket(self):
        return self.my_socket


    """
    FUNCTION
    Will send a challenge response back to another peer once
    it received the challenge from that peer.
    """
    def send_challenge_response(self):
        # generate the nonce
        # encrypt {ID, A's nonce, our session key part} with Master key
        msg = "%s %s" % (str(int.from_bytes(self.crypto.my_nonce, byteorder='little')),
                         self.crypto.encrypt_all())
        return msg