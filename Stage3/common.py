from curve25519 import generatePrivateKey, generatePublicKey, calculateAgreement
from cryptography.fernet import Fernet
import base64
import os
import hmac
import hashlib


def compute_proof(key, data):
    return hmac.new(key, data, digestmod=hashlib.sha256).digest()


def handshake(seed: bytes, socket, password):
    my_private_key = generatePrivateKey(seed)
    my_public_key = generatePublicKey(my_private_key)
    my_nonce = os.urandom(32)

    socket.sendall(my_public_key)
    socket.sendall(my_nonce)

    their_public_key = socket.recv(32)
    their_nonce = socket.recv(32)

    if their_nonce == my_nonce:
        print("Suspecting a replay attack")
        return None
    if their_public_key in (b'\x00' * 32, b'\x01' + (b'\x00' * 31)):
        return None

    shared_key = calculateAgreement(my_private_key, their_public_key)

    my_proof = compute_proof(shared_key, password + their_nonce)
    socket.sendall(my_proof)

    their_proof = socket.recv(32)

    if their_proof != compute_proof(shared_key, password + my_nonce):
        return None

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
