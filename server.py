#!/usr/bin/env python3
import socket
import threading
from datetime import datetime, timezone
import time

HOST = "0.0.0.0"
PORT = 40000  # must be 1025–49151

WELCOME = "WELCOME, I'm TinyServer not pressure\n"

def iso_now_local():
    # Return ISO8601 with local timezone offset (e.g., 2025-09-11T23:10:03-05:00)
    # time.localtime() gives local tzinfo; build offset from tm_gmtoff if available
    # Fallback: naive UTC
    try:
        # Compute local offset
        if time.localtime().tm_isdst and time.daylight:
            offset = -time.altzone
        else:
            offset = -time.timezone
        sign = "+" if offset >= 0 else "-"
        offset_abs = abs(offset)
        hh = offset_abs // 3600
        mm = (offset_abs % 3600) // 60
        tz = f"{sign}{hh:02d}:{mm:02d}"
        return datetime.now().replace(microsecond=0).isoformat() + tz
    except Exception:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def handle_client(conn, addr):
    with conn:
        conn.sendall(WELCOME.encode("utf-8"))
        buffer = b""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                text = line.decode("utf-8", errors="ignore").strip()
                if not text:
                    continue
                parts = text.split(maxsplit=1)
                cmd = parts[0].upper()
                arg = parts[1] if len(parts) > 1 else ""

                if cmd == "TIME":
                    resp = f"TIME {iso_now_local()}\n"
                elif cmd == "ECHO":
                    if not arg:
                        resp = "ERROR BAD_ARGUMENTS\n"
                    else:
                        resp = f"ECHO {arg}\n"
                elif cmd == "HELP":
                    resp = "HELP COMMANDS: TIME | ECHO <TEXT> | QUIT\n"
                elif cmd == "QUIT":
                    conn.sendall(b"BYE\n")
                    return
                else:
                    resp = "ERROR UNKNOWN_COMMAND\n"
                conn.sendall(resp.encode("utf-8"))

def serve():
    print(f"Starting TinyTCP server on {HOST}:{PORT} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Server is listening. Ctrl+C to stop.")
        while True:
            conn, addr = s.accept()
            print(f"Accepted connection from {addr}")
            # For simplicity and this assignment, handle in a thread so multiple clients work
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    try:
        serve()
    except KeyboardInterrupt:
        print("\nServer stopped.")