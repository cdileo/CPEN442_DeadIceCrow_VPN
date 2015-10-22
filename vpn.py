import string
import sys
from VpnClientServer import VpnClientServer
from VpnClient import VpnClient
from CryptoCore import CryptoCore
import getopt
from Crypto import Random
import os

usage= ("\n"
        "Usage\n"
        "-h      show this help message\n"
        "-m      mode of operation\n"
        "        \"server\" for server program\n"
        "        \"client\" for client program\n"
        "        If this setting is given all other arguments are ignored.\n"
        "\n"
        "-s      server IP to connect to (Client mode only)\n"
        "-p      server port\n"
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


    # FLOW

    # read in the symmetric key
    # read in an identifier e,g, "Bob" "Ildar"
    # generate nonces
    # start sending stuff

    crypto = read_keys()

    if not crypto:
        print("Exiting.")
        sys.exit(1)

    # Start client or server
    if op_mode == 1:
        print("[SERVER MODE: starting both client and server]")
        vpn_server = VpnClientServer(port, crypto)
        vpn_server.run_server()

    else:
        print("[CLIENT MODE]")
        print("VpnClient: main: server %s port %d" % (server, port))
        vpn_client = VpnClient(server, port, crypto)
        vpn_client.server = server
        vpn_client.port = port
        print("VpnClient: main: server %s port %d" % (
            vpn_client.server, vpn_client.port))
        vpn_client.start_client()



"""
FUNCTION
 read keys sent
"""
def read_keys():
    # read in the key
    sys.stdout.write("Please enter the key: ")
    sys.stdout.flush()
    temp_key = sys.stdin.readline().rstrip()

    key = pad_key(temp_key)

    print("key is: ")
    print(key)

    # TODO can we store a key inside python object???

    # read in the id
    sys.stdout.write("Please enter your name: ")
    sys.stdout.flush()
    id = sys.stdin.readline().rstrip()

    crypto = CryptoCore(key, id)

    print("SUMMARY: ")
    print("Symmetric key entered %s" % crypto.key)
    print("Name (id) entered %s" % crypto.id)
    print("My nonce generated (32 bits) %d" % int.from_bytes(crypto.my_nonce, byteorder='little') )
    print("\n")

    sys.stdout.write("Continue starting application? [y/n] ")
    sys.stdout.flush()

    answer = sys.stdin.readline()
    answer.replace('\n', '')
    print ("answer given %s" % repr(answer))
    if answer == "y\n":
        return crypto
    if answer == "n\n":
        return 0
    else:
        return -1

"""
FUCTION
pad short key
"""
def pad_key(temp_key):
    if len(temp_key) > 32:
        print("KEY IS TOO LONG. TRY AGAIN. SHUTTING DOWN.")
        sys.exit(1)
    else:
        print("PADDING SHORT KEY")
        return temp_key.zfill(32)



# Run program
if __name__ == "__main__":
    main(sys.argv[1:])