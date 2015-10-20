import threading
import socket
import select
import sys
from Parser import Parser
from enum import Enum

# Constants
BUFFER_SIZE = 4096


class State(Enum):
    Init = 0
    KeyX = 1
    Challenge = 2
    Send = 3


class VpnClient(threading.Thread):

    def __init__(self, server, port, crypto):
        self.server = server
        self.port = port
        self.socket_list = []
        self.my_socket = None
        self.crypto = crypto
        self.state = State.Init

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
                    while self.state != State.Final:
                        if self.state == State.Init:
                            print("INIT")
                            #we're in the key exchange, expecting nonce then id

                            data = sock.recv(BUFFER_SIZE)
                            data = data.decode()
                            # If you can't read - connection interruption - exit
                            if not data:
                                print ('\nDisconnected from chat server')
                                sys.exit()
                            else:
                                parser = Parser()
                                response = parser.parse_data(data)
                                self.crypto.peer_nonce = response[0]
                                self.crypto.id = response[1]
                                self.state = State.KeyX

                        elif self.state == State.KeyX:
                            print("KEYX")
                        #   send challenge response
                            send_data = self.send_challenge_response()
                            sock.send(send_data)
                            self.state = State.Challenge

                        elif self.state == State.Challenge:
                            print("CHALLENGE")
                        #   verify response from 'Alice'
                        else:
                            print("BREAK")
                            break

                    else:
                        print("[ERROR] Authentication failed. Exiting.")
                        sys.exit(1)

                    sys.stdout.write(str(sock.getpeername()))
                    sys.stdout.write(": ")
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

                else:
                    # Read and send user's message
                    msg = sys.stdin.readline()
                    self.mysocket.send(msg.encode())
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
        msg = "%s%s" % (self.crypto.my_nonce, self.crypto.encrypt_all())
        return msg
