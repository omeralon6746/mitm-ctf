import Stage0.server.server as server
import socket
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(
    description='Server runner that accepts a port number')
parser.add_argument('port', type=int, help='Port number to bind the server to')
args = parser.parse_args()


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind(("127.0.0.1", args.port))
tcp_socket.listen(1)

print("Waiting for connection...")

client_socket, _ = tcp_socket.accept()

server.run(
    client_socket,
    os.urandom(32),
    b"flag{EcFlD+WnDq4sDbYNiq/KSyFHV+oV7hRhbRlziwREGyXp}"
)

client_socket.close()
tcp_socket.close()
