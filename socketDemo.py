import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
	errno, strerror = e.args
	print('Failed to create socket. Error code: ' + str(errno) +
		' , Error message: ' + strerror)
	sys.exit();

print ('Socket Created')