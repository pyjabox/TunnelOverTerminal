import os
import getpass
import signal
import subprocess
import argparse
import time
from sys import stdout

parser = argparse.ArgumentParser(description='My example explanation')

parser.add_argument(
    '-s',
    '--port_source',
    default=8765,
    help='provide an integer (default: 8765)'
)

parser.add_argument(
	'-ip',
    '--ip_destination',
    default="127.0.0.1",
    help='provide an ip (default: 127.0.0.1)'
)

parser.add_argument(
	'-d',
    '--port_destination',
    default=22,
    help='provide an integer (default: 22)'
)

parser.add_argument(
	'-f',
    '--force',
    default="no",
    help='provide yes or no (default: no)'
)

parser.add_argument(
    '--clean',
    default="no",
    help='provide brutal or no (default: no)'
)

parser.add_argument(
    '--stats',
    default="no",
    help='provide yes or no (default: no)'
)

params = parser.parse_args()

if params.clean =="brutal":
    eradicate1 = subprocess.Popen("pkill -f netcat -9", shell=True, preexec_fn=os.setsid)
    eradicate1.wait()
    eradicate2 = subprocess.Popen("pkill -f xxd -9", shell=True, preexec_fn=os.setsid)
    eradicate2.wait()
    eradicate3 = subprocess.Popen("pkill -f exp -9", shell=True, preexec_fn=os.setsid)
    eradicate3.wait()

    print "Eradication done. Exiting..."
    exit()


checks = subprocess.Popen("ps aux | egrep 'xxd|netcat|exp' | grep -v grep > /dev/null", shell=True, preexec_fn=os.setsid)
checks.wait()

if checks.returncode==0 and params.force =="no":
    print "Environment may not be clean: xxd,netcat or expect scripts are running"
    print "To try a hard cleaning, use --clean brutal argument. Will kill xxd,netcat and expect running under user ## "+getpass.getuser()+" ##"
    print "To bypass checks, add --force yes argument"
    exit()

proc1 = subprocess.Popen("while :;     do stdbuf -o0 xxd -p -c 1 < fromN > fromN-HEX; done", shell=True, preexec_fn=os.setsid)

if params.stats == "yes":
    proc2 = subprocess.Popen("cat fromN-HEX | tee debug-write.log | ./remote-write.exp > /dev/null", shell=True, preexec_fn=os.setsid)
    proc3 = subprocess.Popen("./remote-read.exp | tee debug-read.log > fromNC-HEX", shell=True, preexec_fn=os.setsid)

else:
    proc2 = subprocess.Popen("cat fromN-HEX | ./remote-write.exp > /dev/null", shell=True, preexec_fn=os.setsid)
    proc3 = subprocess.Popen("./remote-read.exp > fromNC-HEX", shell=True, preexec_fn=os.setsid)

proc4 = subprocess.Popen("while :;     do stdbuf -o0  xxd -p -c 1 -r < fromNC-HEX > toN; done", shell=True, preexec_fn=os.setsid)
proc5 = subprocess.Popen("cat toN | netcat -l -p "+str(params.port_source)+" > fromN", shell=True, preexec_fn=os.setsid)
time.sleep(2)
proc6 = subprocess.Popen("./connect.exp "+str(params.ip_destination)+" "+str(params.port_destination)+" > /dev/null", shell=True, preexec_fn=os.setsid)

print("Press CTRL-C to exit...")

if params.stats == "yes":
    print("Traffic in tunnel (in HEX + Overhead)")
    in_bytes=0
    out_bytes=0
while True:
    try:
        if params.stats == "yes":
            in_bytes=os.path.getsize("debug-read.log")
            out_bytes=os.path.getsize("debug-write.log")
            stdout.write("\r\x1b[K"+"Input bytes= "+str(in_bytes)+" ; Output bytes= "+str(out_bytes))
            stdout.flush()
        time.sleep(1)
        if proc1.poll() is not None:
            print "\r\nTunnel closed. Exiting..."
            break
        if proc2.poll() is not None:
            print "\r\nTunnel closed. Exiting..."
            break
        if proc3.poll() is not None:
            print "\r\nTunnel closed. Exiting..."
            break
        if proc4.poll() is not None:
            print "\r\nTunnel closed. Exiting..."
            break
        if proc5.poll() is not None:
            print "\r\nTunnel closed. Exiting..."
            break
        if proc6.poll() is not None:
            print "\r\nTunnel closed. Exiting..."
            break

    except KeyboardInterrupt:
        break

try:
    os.killpg(proc1.pid, signal.SIGTERM)
except:
    pass
try:
    os.killpg(proc2.pid, signal.SIGTERM)
except:
    pass
try:
    os.killpg(proc3.pid, signal.SIGTERM)
except:
    pass
try:
    os.killpg(proc4.pid, signal.SIGTERM)
except:
    pass
try:
    os.killpg(proc5.pid, signal.SIGTERM)
except:
    pass
try:
    os.killpg(proc6.pid, signal.SIGTERM)
except:
    pass
