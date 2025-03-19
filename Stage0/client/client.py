from Stage0.common import handshake, encrypt, decrypt


def run(socket, private_seed):
    shared_key = handshake(private_seed, socket)

    if shared_key == None:
        print("Handshake failed")
        return None

    print("Handshake complete")

    socket.sendall(encrypt(shared_key, b"Get flag"))
    flag = decrypt(shared_key, socket.recv(1024))

    socket.sendall(encrypt(shared_key, b"Exit"))

    return flag
