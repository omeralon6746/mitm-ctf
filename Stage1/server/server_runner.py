import Stage1.server.server as server
import socket
import os
import argparse
import hashlib

# Set up argument parser
parser = argparse.ArgumentParser(
    description='Server runner that accepts a port number')
parser.add_argument('port', type=int, help='Port number to bind the server to')
args = parser.parse_args()

password = input("Enter the flag from the previous stage: ")

if hashlib.sha256(password.encode()).hexdigest() != '598bf6e1a1b8d2c0a76cf3087253e121b54568777ff01914f21801b56ec14d7d':
    print("Incorrect password")
    exit(1)

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind(("127.0.0.1", args.port))
tcp_socket.listen(1)

print("Waiting for connection...")

client_socket, _ = tcp_socket.accept()

password = int.to_bytes(
    426606250916557431795983626356110631294008115727848805460023387167927233504, 32, 'little')

server.run(
    client_socket,
    os.urandom(32),
    password,
    b"flag{aGVsbG9fZnJvbV9jY29tcGxldGVfY2hlc3N0}"
)

client_socket.close()
tcp_socket.close()
