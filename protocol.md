# TinyTCP Protocol - Client and Server

This project implements a basic **TCP socket communication** system using a custom protocol, with both a server and client. The server responds to client commands with simple messages like the current time or an echo of the client's message. The connection is closed once the client sends a `QUIT` command.

## Project Overview

- **Server**: Listens on a specified port and responds to client commands.
- **Client**: Connects to the server, sends commands, and receives responses.

### Protocol

The protocol uses simple text-based commands sent over TCP, with each message terminated by a newline (`\n`). Commands and responses are case-insensitive.

**Commands:**
1. `TIME` - The server responds with the current date and time in ISO8601 format.
2. `ECHO <TEXT>` - The server echoes the text provided by the client.
3. `HELP` - Lists all available commands.
4. `QUIT` - Terminates the connection and closes it.

### Error Handling
- If the client sends an unknown command, the server will reply with an error message: `ERROR UNKNOWN_COMMAND`.
- If the client sends an `ECHO` command without text, the server replies with: `ERROR BAD_ARGUMENTS`.

## Files Included

- `server.py`: The Python code for the TCP server.
- `client.py`: The Python code for the TCP client.
- `protocol.md`: The protocol documentation (includes the commands and their responses).
- `README.md`: This file, which explains the project, how to run it, and how to interact with the server and client.

### Running the Application

#### 1. Start the Server
In one terminal window, run the server:
```bash
python server.py 
```

The server will start listening on port 40000 (you can change the port if needed, but make sure it's in the range 1025–49151).

#### 2. Run the Client

In another terminal window, run the client:
```bash
python client.py 127.0.0.1 40000
```

This will connect to the server at 127.0.0.1 (localhost) on port 40000. The client will send the following commands:

- TIME - The server will respond with the current time.

- ECHO Hello from client - The server will respond with the same text.

- QUIT - The client will disconnect after receiving BYE from the server.

#### 3. Using Telnet or Netcat (Optional)

You can also use Telnet or Netcat to interact with the server manually.

Telnet:
``` bash telnet 127.0.0.1 40000 ```


After connecting, you can type the commands manually like TIME, ECHO <text>, and QUIT.

##### Result
```
CONNECT to 127.0.0.1:40000
<- WELCOME, I'm TinyServer not pressure
-> TIME
<- TIME 2025-09-12T17:24:13-05:00
-> QUIT
<- BYE
CONNECT to 127.0.0.1:40000
<- WELCOME, I'm TinyServer not pressure
-> ECHO Hello from client
<- ECHO Hello from client
-> QUIT
<- BYE
```

##### Notes

The server handles multiple clients concurrently using threads.

**The client connects twice**: first for the TIME command and then for the ECHO command.

