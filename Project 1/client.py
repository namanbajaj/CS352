import socket
import time

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()
    
# Define the port on which you want to connect to the server
port = 50007
localhost_addr = socket.gethostbyname(socket.gethostname())

# connect to the server on local machine
server_binding = (localhost_addr, port)
cs.connect(server_binding)

# send data to server
string_to_send = "string to send"
cs.send(string_to_send.encode('utf-8'))
print("[C]: Data sent to server: {}".format(string_to_send))

# receive data from the server
data_from_server=cs.recv(100)
print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

time.sleep(1)

data_from_server=cs.recv(100)
print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

time.sleep(2)

# sending contents of file to server
print("[C]: Sending text from file to server")
file = open('in-proj.txt', 'r')
cs.send(file.read().encode('utf-8'))
file.close()

# close the client socket
cs.close()
exit()