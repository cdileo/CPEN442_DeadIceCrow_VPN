import sys
import socket
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

# create socket object. 
def create_connection( host, port ):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print "failed to create socket"
        sys.exit()

    ## TODO remove this host resolution code when connecting on 
    ##  the same network
    try:
        remote_ip = socket.gethostbyname( host )
    except:
        print "could not resolve host"
        sys.exit()

    print "Connecting to host:", host, "port", port, "remote-ip", remote_ip

    try:
        print "connecting"
        s.connect((remote_ip, port))
        return s
    except:
        print("Failed to connect to", host, port, "Switching to standby")
        return 0

    #data = s.recv(4096)
    #print data
    #s.close
    return 0


def wait_for_connection():
    print "waiting for connection"

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
            # mode is
            # connect: connect to peer/server
            # wait: wait for the peer/server to connect to me
            print("Starting in mode", arg)
            exit(1)
        else:
            print("Invalid arguments")
            print(usage)
            sys.exit(1)

    conn_result = create_connection(server, port)
    data = ""

    if ( conn_result == 0 ):
        wait_for_connection()
    else:
        data = conn_result.recv(4096)
        print "printing data from socket"
        print data
        conn_result.close


# DEFINITIONS OVER ##################################################    
# Run program
if __name__ == "__main__":
    main(sys.argv[1:]);
