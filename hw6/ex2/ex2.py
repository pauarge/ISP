from cothority import Cothority
import binascii
import hashlib
import os


URL = "ws://com402.epfl.ch:7003"
GENESIS = "0d8d8f2012b4905b90dd179c060bf56b36fffed4b285067898a642347a9c7621"
EMAIL = "pau.argelaguet@epfl.ch"


def check(nonce, hash_of_last_block, full_email):
    data = nonce + hash_of_last_block + full_email
    m = hashlib.sha256()
    m.update(data)
    d = m.digest()
    return d, data


def main():
    nonce = os.urandom(32)
    blocks = Cothority.getBlocks(URL, binascii.unhexlify(GENESIS))
    hash_of_last_block = blocks[-1].Hash
    full_email = EMAIL.encode('utf-8')

    d, data = check(nonce, hash_of_last_block, full_email)
    while d[0] != 0 or d[1] != 0 or d[2] != 0:
        nonce = os.urandom(32)
        print(d[0], d[1], d[2])
        d, data = check(nonce, hash_of_last_block, full_email)

    block = Cothority.createNextBlock(blocks[-1], data)
    ret = Cothority.storeBlock(URL, block)
    print(ret)


if __name__ == '__main__':
    main()
