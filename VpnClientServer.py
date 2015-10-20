import socket
import select
import sys
from Parser import Parser

BUFFER_SIZE = 4096
PORT = 9009

class VpnClientServer():
    def __init__(self, crypto):
        self.server = ''
        self.port = PORT
        self.socket_list = []
        self.temp_socket = None
        self.server_socket = None
        self.crypto = crypto

    def run_server(self):
        print("run_server: starting server")
        self.temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.temp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.temp_socket.bind((self.server, self.port))
        self.temp_socket.listen(10)

        print ("Chat server started on port %s" % str(PORT))

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


        while 1:

            self.socket_list = [sys.stdin, self.server_socket]

            # last 0 : poll and never block while selecting
            ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[])

            for read_fd in ready_to_read:
                if read_fd == self.server_socket:
                    data = read_fd.recv(BUFFER_SIZE)
                    data = data
                    # If you can't read - connection interruption - exit
                    if not data:
                        print ('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        # print data
                        parser = Parser()
                        parser.parse_data(data)
                        sys.stdout.write(str(read_fd.getpeername()))
                        sys.stdout.write(": ")
                        sys.stdout.write(data)
                        sys.stdout.write('[Me] ')
                        sys.stdout.flush()
                else:
                    # Read and send user's message
                    msg = sys.stdin.readline()
                    self.server_socket.send(msg.encode())
                    sys.stdout.write("[Me] ")
                    sys.stdout.flush()


    # FUNCTION
    # close function
    def close_socket(self):
        self.server_socket.close()