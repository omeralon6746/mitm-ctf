from Stage0.common import handshake, encrypt, decrypt
import socket
import os


def run(socket, private_seed):
    shared_key = handshake(private_seed, socket)

    print("Handshake complete")

    socket.sendall(encrypt(shared_key, b"Get flag"))
    flag = decrypt(shared_key, socket.recv(1024))

    socket.sendall(encrypt(shared_key, b"Exit"))

    return flag


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(("127.0.0.1", 12345))

flag = run(tcp_socket, os.urandom(32))

print(flag)

tcp_socket.close()
