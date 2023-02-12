import sys
import socket

# Get the command line arguments
ts2ListenPort = sys.argv[1]

# Open file corresponding to server file and read it
ts2File = open("PROJ2-DNSTS2.txt", "r")

# Create a socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[ts1]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', int(ts2ListenPort))
ss.bind(server_binding)
ss.listen(1)
host = socket.gethostname()
print("[ts1]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[ts1]: Server IP address is {}".format(localhost_ip))
csockid, addr = ss.accept()
print ("[S]: Got a connection request from a client at {}".format(addr))