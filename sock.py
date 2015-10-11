import sys
import socket

# create socket object. 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print "failed to create socket"
    sys.exit()

host = 'test.dict.org'
port = 2628

try:
    remote_ip = socket.gethostbyname( host )
except:
    print "could not resolve host"
    sys.exit()

print "Host:", host, "port", port, "remote-ip", remote_ip

s.connect((remote_ip, port))

#message = "GET / HTTP/1.1\r\n\r\n"
#s.sendall(message)

print("Connected")
data = s.recv(4096)
print data
s.close
sys.exit(0)
