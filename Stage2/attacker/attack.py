from curve25519 import generatePrivateKey, generatePublicKey, calculateAgreement
from Stage2.common import encrypt, decrypt
import socket
import os


def copied_handshake(seed, socket):
    my_private_key = generatePrivateKey(seed)
    my_public_key = generatePublicKey(my_private_key)

    socket.sendall(my_public_key)
    their_public_key = socket.recv(32)

    their_nonce = socket.recv(32)
    my_nonce = their_nonce
    socket.sendall(my_nonce)

    shared_key = calculateAgreement(my_private_key, their_public_key)

    their_proof = socket.recv(32)
    my_proof = their_proof
    socket.sendall(my_proof)

    return shared_key


def run(socket, private_seed):
    shared_key = copied_handshake(private_seed, socket)

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
