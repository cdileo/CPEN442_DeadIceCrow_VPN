import socket
import select
import threading
import sys

BUFFER_SIZE = 4096
PORT = 9009

class VpnServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = ''
        self.port = PORT
        self.socket_list = []

    def run_server(self):
        print("run_server: starting server")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.server, self.port))
        server_socket.listen(10)

        # add server socket object to the list of readable connections
        self.socket_list.append(server_socket)
        self.socket_list.append(sys.stdin)

        print "Chat server started on port " + str(PORT)

        running = 1

        while running:

            # last 0 : poll and never block while selecting
            ready_to_read,ready_to_write,in_error = select.select(self.socket_list,[],[],0)

            for read_fd in ready_to_read:
                # If a new connection received - accept and add to the list
                #  of sockets already listening to
                if read_fd == server_socket:
                    sockfd, addr = server_socket.accept()
                    self.socket_list.append(sockfd)
                    print ("Client (%s, %s) connected" % addr)

                    self.send_everyone(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

                elif read_fd == sys.stdin:
                    print ("stdin statement")
                    print("[Me]")
                    msg = sys.stdin.readline()
                    self.send_everyone(server_socket, sockfd, msg)

                # Read message from the client - already existing connection
                else:
                    # process data recieved from client,
                    try:
                        # receiving data from the socket.
                        data = read_fd.recv(BUFFER_SIZE)
                        if data:
                            # there is something in the socket
                            self.send_everyone(server_socket, read_fd, "\r" +
                                           '[' + str(read_fd.getpeername()) + '] ' + data)

                            # try sending data to this single socket that's chosen at the moment
                            # Print locally what clients are saying
                            sys.stdout.write('[' + str(read_fd.getpeername()) + '] ' + data)
                            sys.stdout.flush()

                        else:
                            # remove the socket that's broken
                            if read_fd in self.socket_list:
                                self.socket_list.remove(read_fd)

                            # If no data - probably connection interruption
                            self.send_everyone(server_socket, read_fd, "Client (%s, %s) is offline\n" % addr)

                    # exception
                    except:
                        self.send_everyone(server_socket, read_fd, "Client (%s, %s) is offline\n" % addr)
                        continue


        server_socket.close()

    # broadcast chat messages to all connected clients
    def send_everyone (self, server_socket, curr_socket, message):
        for socket in self.socket_list:
            # send to everyone but myself
            if socket != server_socket and socket != curr_socket :
                try :
                    socket.send(message)
                except :
                    # possible connection interruption -> close and remove
                    socket.close()
                    if socket in self.socket_list:
                        self.socket_list.remove(socket)



                            # print("[Me]")
                            # msg = sys.stdin.readline()
                            # self.send_everyone(server_socket, sockfd, msg)

