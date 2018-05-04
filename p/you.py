import socket
import sys

HOST, PORT = "localhost", 9999
account = input("ac")
password = input("pw")

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(account+" "+password, "ascii"))

    # Receive data from the server and shut down
finally:
    sock.close()

