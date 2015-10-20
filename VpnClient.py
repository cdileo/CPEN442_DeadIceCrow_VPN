import threading
import socket
import select
import sys
import string

# Constants
BUFFER_SIZE = 4096


class VpnClient(threading.Thread):

    def __init__(self, server, port):
        threading.Thread.__init__(self)
        self.server = server
        self.port = port
        self.socket_list = []
        self.my_socket = None

    """
    FUNCTIONhttps://raw.githubusercontent.com/cdileo/CPEN442_DeadIceCrow_VPN/master/left.jpg?token=AHQPa8M7BNlNxdwRBhgKSx6xNJ7I1oyIks5WL6hLwA%3D%3D
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
                        p_data = parser.parse_data(data)
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

class Parser():
    """
    FUNCTION
        takes a string and parses it
    """
    def parse_data(self, data):
        data_list = data.split(" ")

        for w in data_list:
            index = 0
            print("%d %s" % (index, repr(w)) )
            index = index + 1

        # The first two indexes are info about the client
        if data_list[0] == '500':
            key = data_list[1]
            print("Recieving challenge: %s" % key)
            return 1
        else:
            print("Got no code - just a regular string.")
            return 0
