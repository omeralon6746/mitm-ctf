from curve25519 import generatePrivateKey, calculateAgreement
from Stage3.common import encrypt, decrypt
import socket
import os


def copied_handshake(seed, client_socket, server_socket):
    my_private_key = generatePrivateKey(seed)
    my_bad_public_key = int.to_bytes(
        325606250916557431795983626356110631294008115727848805560023387167927233504, 32, 'little')

    client_socket.sendall(my_bad_public_key)
    server_socket.sendall(my_bad_public_key)
    their_public_key = server_socket.recv(32)
    their_public_key = client_socket.recv(32)

    client_nonce = client_socket.recv(32)
    server_socket.sendall(client_nonce)

    server_nonce = server_socket.recv(32)
    client_socket.sendall(server_nonce)

    # Giving my public key because it's weak and will generate the same shared key as both parties
    shared_key = calculateAgreement(my_private_key, my_bad_public_key)

    server_proof = server_socket.recv(32)
    client_proof = client_socket.recv(32)

    server_socket.sendall(client_proof)

    # This will fail the client proof check, but we don't care
    client_socket.sendall(client_proof)

    return shared_key


def run(server_socket, client_socket, private_seed):
    shared_key = copied_handshake(private_seed, client_socket, server_socket)

    print("Handshake complete")

    server_socket.sendall(encrypt(shared_key, b"Get flag"))
    flag = decrypt(shared_key, server_socket.recv(1024))

    server_socket.sendall(encrypt(shared_key, b"Exit"))

    return flag


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(("127.0.0.1", 12345))

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind(("127.0.0.1", 1234))
tcp_socket.listen(1)
client_socket, _ = tcp_socket.accept()

flag = run(server_socket, client_socket, os.urandom(32))

print(flag)

server_socket.close()
client_socket.close()
tcp_socket.close()
