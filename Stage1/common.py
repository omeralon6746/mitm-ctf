from curve25519 import generatePrivateKey, generatePublicKey, calculateAgreement
from cryptography.fernet import Fernet
import base64


def handshake(seed: bytes, socket):
    my_private_key = generatePrivateKey(seed)
    my_public_key = generatePublicKey(my_private_key)

    socket.sendall(my_public_key)

    their_public_key = socket.recv(32)

    if their_public_key in (b'\x00' * 32, b'\x01' + (b'\x00' * 31)):
        return None

    shared_key = calculateAgreement(my_private_key, their_public_key)

    return shared_key


def encrypt(key, data):
    if data == None:
        return None

    key = base64.urlsafe_b64encode(key)
    f = Fernet(key)

    return f.encrypt(data)


def decrypt(key, data):
    if data == None:
        return None

    key = base64.urlsafe_b64encode(key)
    f = Fernet(key)

    return f.decrypt(data)
