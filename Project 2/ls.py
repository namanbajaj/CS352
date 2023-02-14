import sys
import socket
import select

# Get the command line arguments
lsListenPort = sys.argv[1]
ts1Hostname = sys.argv[2]
ts1ListenPort = sys.argv[3]
ts2Hostname = sys.argv[4]
ts2ListenPort = sys.argv[5]

# Create a socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[ls]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', int(lsListenPort))
ss.bind(server_binding)
ss.listen(5)
host = socket.gethostname()
print("[ls]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[ls]: Server IP address is {}".format(localhost_ip))

# Connect to ts1
try:
    ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[ls]: ts1 socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

ts1_server_binding = (ts1Hostname, int(ts1ListenPort))  
ts1.connect(ts1_server_binding)
print("[ls]: Connected to ts1")

# Connect to ts2
try:
    ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[ls]: ts2 socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

ts2_server_binding = (ts2Hostname, int(ts2ListenPort))
ts2.connect(ts2_server_binding)
print("[ls]: Connected to ts2")

# Connect to client
csockid, addr = ss.accept()
print("[ls]: Got a connection request from a client at {}".format(addr))

# Recieve data from client constantly
sockets = [ts1, ts2]
while True:
    data_from_client = csockid.recv(200).decode('utf-8')
    print("[ls]: Data recieved from client: {}".format(str(data_from_client).strip()))
    if not data_from_client:
        break
    else:
        # Send data to ts1
        ts1.send(data_from_client.encode('utf-8'))
        print("[ls]: Data sent to ts1: {}".format(data_from_client.strip()))
        # Send data to ts2
        ts2.send(data_from_client.encode('utf-8'))
        print("[ls]: Data sent to ts2: {}".format(data_from_client.strip()))

        # Query ts1 and ts2
        results, _, _ = select.select(sockets, [], [], 5)
        if results:
            for sock in results:
                if sock == ts1:
                    data = ts1.recv(200).decode('utf-8')
                    print("[ls]: Data recieved from ts1: {}".format(data.strip()))
                elif sock == ts2:
                    data = ts2.recv(200).decode('utf-8')
                    print("[ls]: Data recieved from ts2: {}".format(data.strip()))
                csockid.send(data.encode('utf-8'))
                print("[ls]: Data sent to client: {}".format(data.strip()))
        else:
            data = "{} - TIMED OUT".format(data_from_client.strip())
            print("[ls]: Timed out waiting for ts1 and ts2 to respond")
            csockid.send(data.encode('utf-8'))

# Close the server socket
ss.close()
exit()
