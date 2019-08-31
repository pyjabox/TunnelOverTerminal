# Tunnel Over Terminal (ToT)
Tunnel TCP or UDP data stream over a terminal session

# Setup
1/ On source machine, create named pipe (FIFO) :
- mkfifo fromN
- mkfifo toN
- mkfifo fromNC-HEX
- mkfifo fromN-HEX

2/ On target machine, create named pipe (FIFO) :
- mkfifo fromNC
- mkfifo toNC

3/ On source machine, modify the three Expect scripts (connect.exp ; remote-read.exp ; remote-write.exp) to let them connect to target machine automatically. Leave the last "send", "expect" and "interact" functions as is.

# Usage

usage: ToT.py [-h] [-s PORT_SOURCE] [-ip IP_DESTINATION] [-d PORT_DESTINATION]
              [-f FORCE] [--clean CLEAN] [--stats STATS]

optional arguments:
  -h, --help            show this help message and exit
  -s PORT_SOURCE, --port_source PORT_SOURCE
                        provide an integer (default: 8765)
  -ip IP_DESTINATION, --ip_destination IP_DESTINATION
                        provide an ip (default: 127.0.0.1)
  -d PORT_DESTINATION, --port_destination PORT_DESTINATION
                        provide an integer (default: 22)
  -f FORCE, --force FORCE
                        provide yes or no (default: no)
  --clean CLEAN         provide brutal or no (default: no)
  --stats STATS         provide yes or no (default: no)

# Example

Terminal 1 : 
user@mylocalhost:~$ python ./ToT.py -s 8765 -ip 127.0.0.1 -d 22 --stats yes
Press CTRL-C to exit...
Traffic in tunnel (in HEX + Overhead)
Input bytes= 164 ; Output bytes= 0

Terminal 2 :
user@mylocalhost:~$ ssh remoteuser@localhost -p 8765
cisco@localhost's password:
Welcome to Remote Host Server

Last login: Sat Aug 31 17:28:05 2019 from 10.60.2.100
remoteuser@remotehost:~$

SSH connection will be encapsulated over the Expect scripts, whatever is in the middle.

# Use cases

- Going through custom bastion hosts which prevent any kind of tunneling. As long as the connection can be done through a traditional Expect script and you land on terminal, we are good to go.

- Doing port redirection from remote network to a local port in local network. Thanks to that you can access web application, Java application, create a Reverse SSH connection...

- Transfer files over this tunnel. SCP will work fine and at a decent rate (~200KB/s)

# Requirements

On local host:
- Python 2.7.16
- Standard Linux binaries (mkfifo, xxd, netcat, expect)

On remote host:
- Standard Linux binaries (mkfifo, xxd, netcat)
