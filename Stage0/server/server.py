from Stage0.common import handshake, encrypt, decrypt


def run(socket, private_seed, flag):
    shared_key = handshake(private_seed, socket)

    if shared_key == None:
        print("Handshake failed")
        return None

    print("Handshake complete")

    request = b""

    while request != b"Exit":
        request = decrypt(shared_key, socket.recv(1024))

        if request == b"Get flag":
            socket.sendall(encrypt(shared_key, flag))
