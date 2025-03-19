from Stage2.common import handshake, encrypt, decrypt


def run(socket, private_seed, password, flag):
    shared_key = handshake(private_seed, socket, password)

    if shared_key == None:
        print("Handshake failed")
        return

    request = b""

    while request != b"Exit":
        request = decrypt(shared_key, socket.recv(1024))

        if request == b"Get flag":
            socket.sendall(encrypt(shared_key, flag))
