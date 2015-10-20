import threading
import socket
import select
import sys
from Parser import Parser

# Constants
BUFFER_SIZE = 4096


class VpnClient(threading.Thread):

    def __init__(self, server, port, crypto):
        self.server = server
        self.port = port
        self.socket_list = []
        self.my_socket = None
        self.crypto = crypto

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
                    data = sock.recv(BUFFER_SIZE)
                    data = data.decode()
                    # If you can't read - connection interruption - exit
                    if not data:
                        print ('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        # print data
                        parser = Parser()
                        response = parser.parse_data(data)

                        if response:
                            self.send_challenge_response()
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
        # TODO we need to send an IV
        # encrpt {ID, A's nonce, our session key part} with Master key
        msg = self.nonce + self.crypto.encrypt_all
        return
