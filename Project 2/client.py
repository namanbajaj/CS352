import sys
import socket

# Get the command line arguments
lsHostname = sys.argv[1]
lsListenPort = sys.argv[2]

# Open file that contains domain names to query from ls
lsFile = open("PROJ2-HNS.txt", "r")
dnsQueries = lsFile.readlines()
lsFile.close()

# Open file that will write the results of the queries
resultsFile = open("RESOLVED.txt", "w+")

# Connect to ls
try:
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[client]: ls socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

ls_server_binding = (lsHostname, int(lsListenPort))
ls.connect(ls_server_binding)
print("[client]: Connected to ls")

# Send data to ls
for query in dnsQueries:
    ls.send(query.encode('utf-8'))
    print("[client]: Data sent to ls: {}".format(query).strip())
    data_from_ls = ls.recv(200).decode('utf-8')
    print("[client]: Data recieved from ls: {}".format(data_from_ls).strip())
    resultsFile.write(data_from_ls.strip())
    resultsFile.write("\n")

resultsFile.close()
ls.close()
# ss.close()
exit()