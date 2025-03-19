from Stage1.common import handshake, encrypt, decrypt
import socket
import os


def get_password():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind(("127.0.0.1", 1234))
    tcp_socket.listen(1)
    client_socket, _ = tcp_socket.accept()

    shared_key = handshake(os.urandom(32), client_socket)

    password = decrypt(shared_key, client_socket.recv(1024))
    client_socket.sendall(encrypt(shared_key, b"Wrong password"))

    client_socket.close()
    tcp_socket.close()

    # Get the password
    return password


def get_flag(password):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect(("127.0.0.1", 12345))

    shared_key = handshake(os.urandom(32), tcp_socket)

    print("Handshake complete")

    tcp_socket.sendall(encrypt(shared_key, password))
    response = decrypt(shared_key, tcp_socket.recv(1024))

    if response != b"OK":
        print("Login failed")
        return ""

    tcp_socket.sendall(encrypt(shared_key, b"Get flag"))
    flag = decrypt(shared_key, tcp_socket.recv(1024))

    tcp_socket.sendall(encrypt(shared_key, b"Exit"))

    return flag


password = get_password()

print(get_flag(password))
