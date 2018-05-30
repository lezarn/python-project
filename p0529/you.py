import socket
import sys

HOST, PORT = "localhost", 9999
fuction=""

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    while fuction != "off":
        fuction = input("功能")
        sock.sendall(bytes(fuction, "ascii"))
        print(str(sock.recv(1024),"ascii"))

    # Receive data from the server and shut down
finally:
    sock.close()

