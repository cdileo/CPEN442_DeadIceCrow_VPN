import string
import sys
from VpnClient import VpnClient
from VpnServer import VpnServer
import getopt

from tkinter import *
from tkinterExample import Application 

def main():
    root = Tk()
    app = Application(master = root)
    app.mainloop()

    op_mode = app.mode.get()
    host = app.host.get()
    port = int(app.port.get())
    # print(op_mode)
    # print(host)
    # print(port)

    # Start client or server
    if op_mode == 1:
        print("[SERVER MODE: starting both client and server]")
        #server = "192.168.0.22"
        #port = 9009

        vpn_server = VpnServer(host, port)
        #vpn_client = VpnClient(server, port)
        vpn_server.run_server()

        #""" starting client on same machine as server """
        #vpn_client.start_client()

        print ("vpn: main: local client started on separate thread")
    else:
        print("[CLIENT MODE]")
        print("VpnClient: main: server %s port %d" % (host, port))
        vpn_client = VpnClient(host, port)
        vpn_client.host = host
        vpn_client.port = port
        print("VpnClient: main: server %s port %d" % (vpn_client.host, vpn_client.port))
        vpn_client.start_client()

# Run program
if __name__ == "__main__":
    main()