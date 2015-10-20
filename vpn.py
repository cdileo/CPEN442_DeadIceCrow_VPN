import string
import sys
from VpnClientServer import VpnClientServer
from VpnClient import VpnClient
import getopt

usage= ("\n"
        "Usage\n"
        "-h      show this help message\n"
        "-m      mode of operation\n"
        "        \"server\" for server program\n"
        "        \"client\" for client program\n"
        "        If this setting is given all other arguments are ignored.\n"
        "\n"
        "-s      server IP to connect to (Client mode only)\n"
        "-p      server port (Client mode only)\n"
        "\n"
        "Client example:\n"
        "    python chat.py -m client -s 192.168.0.22 -p 6000\n"
        "\n"
        "Server example:\n"
        "    python chat.py -m server\n"
        "    All settings for server and port will be ignored.\n")

def main(argv):
    op_mode = 0

    try:
        opts, args = getopt.getopt(argv, "hs:p:S")
        if len(argv) == 0:
            print(usage)
    except:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h"):
            print(usage)

        # server IP
        elif opt in ("-s"):
            print("Server IP", arg)
            server = arg

        # port number
        elif opt in ("-p"):
            print("Port number", arg)
            port = int(arg)

        # Mode of operation: {server, client}
        elif opt in ("-S"):
            print("Starting server mode %s" % arg)
            op_mode = 1

        # Error case
        else:
            print("Invalid arguments")
            print(usage)
            sys.exit(1)


    # if read_keys() != 1:
    #     print("Exiting.")
    #     sys.exit(1)

    # Start client or server
    if op_mode == 1:
        print("[SERVER MODE: starting both client and server]")
        #server = "192.168.0.22"
        #port = 9009

        vpn_server = VpnClientServer()
        #vpn_client = VpnClient(server, port)
        vpn_server.run_server()

        #""" starting client on same machine as server """
        #vpn_client.start_client()

        print ("vpn: main: local client started on separate thread")
    else:
        print("[CLIENT MODE]")
        print("VpnClient: main: server %s port %d" % (server, port))
        vpn_client = VpnClient(server, port)
        vpn_client.server = server
        vpn_client.port = port
        print("VpnClient: main: server %s port %d" % (vpn_client.server, vpn_client.port))
        vpn_client.start_client()



"""
FUNCTION
 read keys sent
"""
def read_keys():
    sys.stdout.write("Please enter the key: ")
    sys.stdout.flush()
    key = sys.stdin.readline()
    print("key entered %s" % key)

    sys.stdout.write("Continue starting application? [y/n] ")
    sys.stdout.flush()

    answer = sys.stdin.readline()
    answer.replace('\n', '')
    print ("answer given %s" % repr(answer))
    if answer == "y\n":
        return 1
    if answer == "n\n":
        return 0
    else:
        return -1


# Run program
if __name__ == "__main__":
    main(sys.argv[1:])