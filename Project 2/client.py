import sys
import socket

# Get the command line arguments
lsHostname = sys.argv[1]
lsListenPort = sys.argv[2]

# Open file that contains domain names to query from ls
lsFile = open("PROJ2-HNS.txt", "r")

# Open file that will write the results of the queries
resultsFile = open("RESOLVED.txt", "w+")

# Create a socket
