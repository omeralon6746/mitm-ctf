import Stage3.client.client as client
import socket
import os
import argparse


parser = argparse.ArgumentParser(
    description='Client runner that accepts a port number')
parser.add_argument(
    'port', type=int, help='Port number to connect to server with')
args = parser.parse_args()

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(("127.0.0.1", args.port))

password = int.to_bytes(
    426606250916557431795983626356110631294008115727848805460023387167927233504, 32, 'little')

flag = client.run(
    tcp_socket,
    os.urandom(32),
    password,
)

tcp_socket.close()
