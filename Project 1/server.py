import socket
import time

from random import random

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

time.sleep(2)

file_text = csockid.recv(200)
print("[S]: Recieved message from client")
print("[S]: Writing cases out to files")

# print(file_text)

file_reverse = open('outr-proj.txt', 'w+')
file_upper = open('outup-proj.txt', 'w+')

cur_line = ""
for c in file_text:
    if c == '\n' and cur_line != "":
        # print(cur_line)
        cur_line = cur_line.strip()
        file_reverse.write(cur_line[::-1])
        file_upper.write(cur_line.upper())
        file_reverse.write('\n')
        file_upper.write('\n')
        cur_line = ""
    else:
        cur_line += c
if cur_line != "":
    file_reverse.write(cur_line[::-1])
    file_upper.write(cur_line.upper())

# print(file_text)

# Close the server socket
ss.close()
exit()