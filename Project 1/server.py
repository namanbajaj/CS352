import socket
import time

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', 50007)
ss.bind(server_binding)
ss.listen(1)
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = ss.accept()
print ("[S]: Got a connection request from a client at {}".format(addr))

# send a intro message to the client.  
# msg = "Welcome to CS 352!"
# csockid.send(msg.encode('utf-8'))

# read in data from client
msg = csockid.recv(100)
print("[S]: Recieved string from client: [{}]".format(msg))

# modifying string
msg_rev = msg[::-1]
print("[S]: Reversing string from client and sending it back: [{}]".format(msg_rev))
csockid.send(msg_rev.encode('utf-8'))

time.sleep(1)

msg_cap = msg.upper()
print("[S]: Capitalizing string from client and sending it back: [{}]".format(msg_cap))
csockid.send(msg_cap.encode('utf-8'))

# Close the server socket
ss.close()
exit()