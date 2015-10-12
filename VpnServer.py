import socket
import select
import threading
import sys

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
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
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)

        # add server socket object to the list of readable connections
        SOCKET_LIST.append(server_socket)

        print "Chat server started on port " + str(PORT)

        while 1:

            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

            for sock in ready_to_read:
                # a new connection request recieved
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    SOCKET_LIST.append(sockfd)
                    print ("Client (%s, %s) connected" % addr)

                    self.send_everyone(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

                # a message from a client, not a new connection
                else:
                    # process data recieved from client,
                    try:
                        # receiving data from the socket.
                        data = sock.recv(RECV_BUFFER)
                        if data:
                            # there is something in the socket
                            self.send_everyone(server_socket, sock, "\r" +
                                           '[' + str(sock.getpeername()) + '] ' + data)

                            # try sending data to this single socket that's chosen at the moment
                            print("[Me]")
                            msg = sys.stdin.readline()
                            sock.send(msg)

                        else:
                            # remove the socket that's broken
                            if sock in SOCKET_LIST:
                                SOCKET_LIST.remove(sock)

                            # at this stage, no data means probably the connection has been broken
                            self.send_everyone(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

                    # exception
                    except:
                        self.send_everyone(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                        continue

        server_socket.close()

    # broadcast chat messages to all connected clients
    def send_everyone (self, server_socket, sock, message):
        for socket in SOCKET_LIST:
            # send the message only to peer
            if socket != server_socket and socket != sock :
                try :
                    socket.send(message)
                except :
                    # broken socket connection
                    socket.close()
                    # broken socket, remove it
                    if socket in SOCKET_LIST:
                        SOCKET_LIST.remove(socket)
