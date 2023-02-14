import sys
import socket

# Get the command line arguments
ts1ListenPort = sys.argv[1]

# Open file corresponding to server file and read it
ts1File = open("PROJ2-DNSTS1.txt", "r")
dnsTable = {}
for line in ts1File:
    line = line.strip()
    line = line.split()
    temp = line[0].lower()
    dnsTable[temp] = line[0] + " " + line[1]
    # print(line)
print(dnsTable)


# Create a socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[ts1]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', int(ts1ListenPort))
ss.bind(server_binding)
ss.listen(5)
host = socket.gethostname()
print("[ts1]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[ts1]: Server IP address is {}".format(localhost_ip))

# Connect to ls
csockid, addr = ss.accept()
print ("[ts1]: Got a connection request from a client at {}".format(addr))

# Recieve data from ls constantly
while True:
    data_from_ls = csockid.recv(200).decode('utf-8')
    if not data_from_ls:
        break
    else:
        print("[ts1]: Data recieved from ls: {}".format(str(data_from_ls).strip()))
        # Send data to ls
        data_from_ls = data_from_ls.strip()
        temp = data_from_ls.lower()
        if temp in dnsTable.keys():
            data_to_ls = dnsTable[temp] + " A IN"
            csockid.send(data_to_ls.encode('utf-8'))
            print("[ts1]: Data sent to ls: {}".format(data_to_ls))
        else:
            # data_to_ls = "Error:HOST NOT FOUND"
            # csockid.send(data_to_ls.encode('utf-8'))
            print("[ts1]: No data sent to ls")

# Close the server socket
ss.close()
exit()