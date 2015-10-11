# chat_client.py

import sys
import socket
import select
import getopt

usage="""
Usage
-h      show this help message
-m      mode of operation
        "server" for server program
        "client" for client program
        If this setting is given all other arguments are ignored.

-s      server IP to connect to (Client mode only)
-p      server port (Client mode only)

Client example:
    python chat.py -m client -s 192.168.0.22 -p 6000

Server example:
    python chat.py -m server -s 192.168.0.22 -p 6000
    All settings for server and port will be ignored.
"""


def chat_client(host, port):
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port'
        sys.exit()

    print("host", host, "port", port)

    # create socket to connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect: check provided host name, port and make sure server is up'
        sys.exit()

    print "Connection established"
    sys.stdout.write('Me: ');
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); 
                    sys.stdout.flush()

            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                #sys.stdout.write('[Me] '); 
                print('Me:')
                #sys.stdout.flush()


# Program starts here
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:p:m:")
        if len(argv) == 0:
            print(usage)
    except:
        print(usage)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h"):
            print(usage)
        elif opt in ("-s"):
            print("Server IP", arg)
            server = arg
        elif opt in ("-p"):
            print("Port number", arg)
            port = int(arg)
        elif opt in ("-m"):
            print("Starting in mode", arg)
            exit(1)
        else:
            print("Invalid arguments")
            print(usage)
            sys.exit(1)

    sys.exit(chat_client(server, port))


# DEFINITIONS OVER ##################################################    
# Run program
if __name__ == "__main__":
    main(sys.argv[1:]);
