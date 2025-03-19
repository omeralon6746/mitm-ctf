import os
from curve25519 import generatePrivateKey, generatePublicKey, calculateAgreement
from binascii import hexlify

keys = set()

for i in range(30):
    private = os.urandom(32)
    private = generatePrivateKey(private)

    bad_public = int.to_bytes(
        325606250916557431795983626356110631294008115727848805560023387167927233504, 32, 'little')

    shared = calculateAgreement(private, bad_public)
    print(hexlify(shared))
    keys.add(shared)

print("[~] Num of different keys: {}".format(len(keys)))
