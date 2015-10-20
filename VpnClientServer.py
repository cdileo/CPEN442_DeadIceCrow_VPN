import socket
import select
import threading
import sys
import string

BUFFER_SIZE = 4096
PORT = 9009

class VpnClientServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = ''
        self.port = PORT
        self.socket_list = []
        self.temp_socket = None
        self.server_socket = None

    def run_server(self):
        print("run_server: starting server")
        self.temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.temp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.temp_socket.bind((self.server, self.port))
        self.temp_socket.listen(10)

        print ("Chat server started on port %s" % str(PORT))

        # establish a connection
        sockfd, addr = self.temp_socket.accept()
        print ("Client (%s, %s) connected" % addr)

        self.server_socket = sockfd

        print("Connection established")
        sys.stdout.write("[Me] ")
        sys.stdout.flush()

        while 1:

            self.socket_list = [sys.stdin, self.server_socket]

            # last 0 : poll and never block while selecting
            ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[])

            for read_fd in ready_to_read:
                if read_fd == self.server_socket:
                    data = read_fd.recv(BUFFER_SIZE)
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
                    self.server_socket.send(msg)
                    sys.stdout.write("[Me] ")
                    sys.stdout.flush()

    # self.server_socket.close()




class Parser():
    """
    FUNCTION
        takes a string and parses it
    """
    def parse_data(self, data):
        data_list = string.split(data, " ")

        for w in data_list:
            index = 0
            print("%d %s" % (index, repr(w)) )
            index = index + 1

        # The first two indexes are info about the client
        if data_list[0] == '500':
            key = data_list[1].decode(encoding="UTF-8")
            print("Recieving key: %s" % key)
            return 1
        else:
            print("Got no code - just a regular string.")
            return 0