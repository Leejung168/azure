#!/usr/bin/python
# Start network trace when detecting 404 errors in Squid log.
# 2019-04-25 Lambert.Li Init

import os

#Squid Log file location.
LogFile = "/root/time.txt"

#State file, used to store the File offset.
StateFile = "/tmp/squid.tmp"

# if the count is greater than the value below, then trigger the network trace.
Count = 1

# Check State File set
def checkoffset(StateFile):
    try:
        statefile = open(StateFile, "r+")
        offset = statefile.read()
    except IOError:
        statefile = open(StateFile, "w+")
        statefile.write("0")
        statefile.close()
        offset = 0
    return offset

# Load log and run network capture
def main(LogFile, StateFile):
    count = 0
    of=int(checkoffset(StateFile))
    try:
        logfile = open(LogFile, "r+")
        logfile.seek(of)
        logs = logfile.read()
        # Update the fileoffset
        statefile = open(StateFile, "w+")
        statefile.write(str(logfile.tell()))
        statefile.close()
    except IOError:
        logfile = open(LogFile, "w+")
        print logfile.write("Ops, The file doesn't exist.")
        logs = "nothing"
    finally:
        logfile.close()

    if logs != "nothing":
       logss = logs.split("\n")
       for i in logss:
           if "TCP_MISS/404" in i:
               count = count + 1

    if count > Count:
       # Run network trace 180s.
       os.system("sudo tcpdump -G 180 -W 1 -w /tmp/`hostname`+`date +%Y%m%d-%H%M`.pcap")
    return count

if __name__ == "__main__":
    main(LogFile, StateFile)
