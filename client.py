#!/usr/bin/env python3
import socket
import sys

def read_line(sock):
    buf = b""
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            break
        buf += chunk
    line, _, rest = buf.partition(b"\n")
    return line.decode("utf-8", errors="ignore")

def talk(host, port, commands):
    print(f"CONNECT to {host}:{port}")
    with socket.create_connection((host, port), timeout=5) as sock:
        banner = read_line(sock)
        print(f"<- {banner}")
        for cmd in commands:
            print(f"-> {cmd}")
            sock.sendall((cmd + "\n").encode("utf-8"))
            resp = read_line(sock)
            print(f"<- {resp}")
            if cmd.strip().upper() == "QUIT":
                break

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py <HOST> <PORT>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])

    # First connection: TIME then QUIT
    talk(host, port, ["TIME", "QUIT"])

    # Second connection: ECHO then QUIT
    talk(host, port, ["ECHO Hello from client", "QUIT"])