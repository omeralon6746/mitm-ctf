from Stage1.common import handshake, encrypt, decrypt


def run(socket, private_seed, password):
    shared_key = handshake(private_seed, socket)

    if shared_key == None:
        print("Handshake failed")
        return None

    # Login
    socket.sendall(encrypt(shared_key, password))
    response = decrypt(shared_key, socket.recv(1024))

    if response != b"OK":
        print("Login failed")
        return None

    socket.sendall(encrypt(shared_key, b"Get flag"))
    flag = decrypt(shared_key, socket.recv(1024))

    socket.sendall(encrypt(shared_key, b"Exit"))

    return flag
