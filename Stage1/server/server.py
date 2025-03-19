from Stage1.common import handshake, encrypt, decrypt


def run(socket, private_seed, password, flag):
    shared_key = handshake(private_seed, socket)

    if shared_key == None:
        print("Handshake failed")
        return None

    # Verify user
    received_password = decrypt(shared_key, socket.recv(1024))

    if received_password != password:
        socket.sendall(encrypt(shared_key, b"Wrong password"))
        return
    socket.sendall(encrypt(shared_key, b"OK"))

    request = b""

    while request != b"Exit":
        request = decrypt(shared_key, socket.recv(1024))

        if request == b"Get flag":
            socket.sendall(encrypt(shared_key, flag))
