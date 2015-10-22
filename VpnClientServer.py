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
        # TODO wrap into try-except
        sockfd, addr = self.temp_socket.accept()
        print ("Client (%s, %s) connected" % addr)

        self.server_socket = sockfd

        print("Connection established")
        sys.stdout.write("[Me] ")
        sys.stdout.flush()


        # call a function that will send all challenge: nonce and ID
        #         print(self.crypto.my_nonce)
        # struct.unpack("<L", b'\xa7\xa5Ah')[0]


        init_msg = str(int.from_bytes(self.crypto.my_nonce, byteorder='little')) + \
                   " " + str(self.crypto.id)
        # init_msg.append(" ")                    # string
        # init_msg = (" " + str(self.crypto.id))    # string
        self.server_socket.send(init_msg.encode())
        self.state = State.KeyX


        while 1:

            self.socket_list = [sys.stdin, self.server_socket]


            # last 0 : poll and never block while selecting
            ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[])

            for sock in ready_to_read:
                if sock == self.server_socket:


                    # If you can't read - connection interruption - exit

                    if self.state != State.Final:
                        data = sock.recv(BUFFER_SIZE)
                        while self.state != State.Final:

                            if self.state == State.Init:
                                print("hannah is cool")

                            elif self.state == State.KeyX:
                                print("KEYX")
                                # send challenge response - encryptta
                                #print(len(data.decode()))
                                #print("server data len %d" % len(data))

                                parser = Parser()
                                # reponse is a list of string
                                response = parser.parse_data(data)
                                print("RESPONSE")
                                print(response)
                                print("nonce is %s" % response[0])
                                self.crypto.peer_nonce = str(response[0])
                                print("PEER NONCE")
                                print(self.crypto.peer_nonce)
                                
                                temp = parser.parse_byte_string(data)
                                plain = self.crypto.decrypt_all(temp[1].encode())
                                print("PLAIN")
                                print(plain)

                                nonce_and_msg = parser.parse_plaintxt(plain)
                                print(nonce_and_msg)

                                print(self.crypto.my_nonce)
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
                                print("We know its Alice")
                                print("BREAK")
                                break


                    else:
                        data = sock.recv(BUFFER_SIZE)
                        if not data:
                            print ('\nDisconnected from chat server')
                            sys.exit()
                        else:

                            # print data
                            # WOKRING CHAT
                            print("SERVER OUT OF LOOP")
                            parser = Parser()
                            #parser = Parser()
                            #parser.parse_data(data)
                            sys.stdout.write(str(sock.getpeername()))
                            sys.stdout.write(": ")
                            # decrypt here
                            decrypted_msg = self.crypto.cipher.decrypt(data)
                            print(decrypted_msg)
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
                    # encrypt here
                    encrypted_msg = self.crypto.cipher.encrypt(msg)
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
        print("SERVER SEND CHALLENGE RESPONSE msg is %s" % msg)
        return msg