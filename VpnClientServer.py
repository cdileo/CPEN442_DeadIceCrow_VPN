import socket
import select
import sys
from Parser import Parser
from enum import Enum
import struct

BUFFER_SIZE = 4096
#PORT = 9009

class State(Enum):
    Init = 0
    KeyX = 1
    Challenge = 2
    Final = 3

class VpnClientServer():
    def __init__(self, port, crypto):
        self.server = ''
        self.port = port
        self.socket_list = []
        self.temp_socket = None
        self.server_socket = None
        self.crypto = crypto
        self.state = State.Init
        self.destructCount = 10

    def run_server(self):
        print("run_server: starting server")
        self.temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.temp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.temp_socket.bind((self.server, self.port))
        self.temp_socket.listen(10)

        print ("Chat server started on port %s" % str(self.port))

        # establish a connection
        sockfd, addr = self.temp_socket.accept()
        print ("Client (%s, %s) connected" % addr)

        self.server_socket = sockfd

        print("Connection established")
        sys.stdout.write("[Me] ")
        sys.stdout.flush()

        init_msg = str(int.from_bytes(self.crypto.my_nonce, byteorder='little')) + \
                   " " + str(self.crypto.id)

        self.server_socket.send(init_msg.encode())
        self.state = State.KeyX


        while 1:

            self.socket_list = [sys.stdin, self.server_socket]

            # last 0 : poll and never block while selecting
            ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[])

            for sock in ready_to_read:
                if sock == self.server_socket:

                    if self.state != State.Final:
                        data = sock.recv(BUFFER_SIZE)
                        while self.state != State.Final:

                            if self.state == State.Init:
                                print("hannah is cool")

                            elif self.state == State.KeyX:
                                print("P is "+str(self.crypto.p))
                                print("G is "+str(self.crypto.g))

                                parser = Parser()
                                # reponse is a list of string
                                response = parser.parse_data(data)

                                self.crypto.peer_nonce = str(response[0])
                                
                                temp = parser.parse_byte_string(data)
                                plain = self.crypto.decrypt_all(temp[1].encode())

                                nonce_and_msg = parser.parse_plaintxt(plain)

                                if int(nonce_and_msg[1]) != struct.unpack("<L",self.crypto.my_nonce)[0]:
                                    print("[ERROR] Not my nonce, man.")
                                    sys.exit(1)
                                else:
                                    print("verified nonce!")
                                    send_data = self.send_challenge_response()
                                    sock.send(send_data.encode())
                                    self.crypto.session_key = (int(nonce_and_msg[2])**self.crypto.A) % self.crypto.p
                                    self.state = State.Final
                                continue

                            else:
                                print("BREAK")
                                break


                    else:
                        data = sock.recv(BUFFER_SIZE)
                        if not data:
                            print ('\nDisconnected from chat server')
                            sys.exit()
                        else:

                            parser = Parser()
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
                    # Read and send user's message
                    if self.destructCount > 0:
                        self.destructCount -= 1
                    else:
                        print ("Hit our maximum number of messages. Terminating to protect forward secrecy.")
                        print ("Have a nice day :)")
                        sys.exit(0)
                    msg = sys.stdin.readline()
                    encrypted_msg = self.crypto.cipher.encrypt(msg)
                    print("encrypted message to be sent ", encrypted_msg)
                    self.server_socket.send(encrypted_msg)
                    sys.stdout.write("[Me] ")
                    sys.stdout.flush()


    # FUNCTION
    # close function
    def close_socket(self):
        self.server_socket.close()


    """
    FUNCTION
    Will send a challenge response back to another peer once
    it received the challenge from that peer.
    works only for step 3
    """
    def send_challenge_response(self):
        # generate the nonce
        # encrypt {ID, A's nonce, our session key part} with Master key
        msg = "%s" % (self.crypto.encrypt_all())
        return msg