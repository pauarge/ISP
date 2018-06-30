#!/usr/bin/env python3

import sys
import string
import random
import time
import hashlib
import socket
import binascii
import os

from functools import reduce

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits

AES_KEY_SIZE = 32
AES_IV_SIZE = AES.block_size
AES_MODE = AES.MODE_CBC

CHAT_MSG_LEN = 64
CHAT_MSG_BODY_LEN = 44
CHAT_MSG_INDEX_LEN = 20
NUMBER_OF_CHAT_MSGS = 10

PRIMARY_SERVER_ID = 0


class ServerData:
    server_id = None
    public_key = None
    shared_key = None
    server_ip = None
    udp_port = None

    def __init__(self, server_id, public_key, shared_key, server_ip, udp_port):
        self.server_id = server_id
        self.public_key = public_key
        self.shared_key = shared_key
        self.server_ip = server_ip
        self.udp_port = udp_port


def read_server_data():
    # Read data about the servers from a file
    servers_filename = 'all_servers.txt'

    all_servers = []
    with open(servers_filename, 'r') as fp:
        for line in fp.readlines():
            server_id = int(line.split()[0])
            server_ip = line.split()[1]
            udp_port = int(line.split()[2])

            all_servers.append(ServerData(server_id, None, None, server_ip, udp_port))

    return all_servers


# Onion encrypt provided message, with server shared keys in reverse order.
# result = enc_k0(...enc_km-1(enc_km(msg))...)
# Encryption algorithm: AES
# Encryption mode: AES_MODE = AES.MODE_CBC
# Docs: https://www.dlitz.net/software/pycrypto/api/current/Crypto-module.html
# Example of AES encryption:
#   iv = Random.new().read(AES_IV_SIZE)
#   cipher = iv + AES.new(key, AES_MODE, iv).encrypt(plain)
def onion_encrypt_message(msg, servers):
    cipher = msg
    for server in reversed(servers):
        iv = Random.new().read(AES_IV_SIZE)
        cipher = iv + AES.new(server.shared_key, AES_MODE, iv).encrypt(cipher)
    return cipher


# Onion decrypt provided ciphertext
# See the explanation for the ecnryption
def onion_decrypt_message(cip, servers):
    print("Onion decrypt message")
    # TODO: insert your code here!
    pass


def rsa_encrypt(msg, pub_key):
    return pub_key.encrypt(msg, None)[0]


# Sends a message to the server
# Important: Expects a response from the server
# Input argument msg should be a string
def send_msg_to_server(server, msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (server.server_ip, server.udp_port))

    data = None
    sock.settimeout(1)
    try:
        data, other = sock.recvfrom(4096)
    except socket.timeout:
        print('UDP receive request from server %d timed-out' % server.server_id)
    finally:
        sock.close()

    return data


# Sends a message to the server
# Doesn't expect a response from server
# Input argument msg should be a string
def send_msg_to_server_async(server, msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (server.server_ip, server.udp_port))
    sock.close()


def generate_random_message(msg_len):
    return ''.join([random.choice(char_set) for _ in range(msg_len)])


# Generates random chat messages of the following format:
# first CHAT_MSG_INDEX_LEN characters represent msg index
# next  CHAT_MSG_BODY_LEN characters are the message itself
def generate_chat_messages(num_msg):
    messages = []
    for i in range(num_msg):
        msg = generate_random_message(CHAT_MSG_BODY_LEN)
        msg_idx = str(i).zfill(CHAT_MSG_INDEX_LEN)
        messages.append(msg_idx + msg)
    return messages


# Client which is responsible for:
#   - Generate and send a shared key to each server
#   - Generate chat messages, onion-encrypt them and
#     send them to the primary server
def client_sender(servers, num_messages):
    # Generate and exchange shared key with each server
    # Generated shared key should be encrypted with server's
    # public key before sending (see server_skeleton script
    # for the expected format of shared key)
    for server in servers:
        pk = send_msg_to_server(server, "pubkey_req")
        server.public_key = RSA.importKey(pk)
        server.shared_key = hashlib.sha256(os.urandom(AES_KEY_SIZE)).digest()
        print("Shared key of server", server.server_id, server.shared_key)
        enc = rsa_encrypt(server.shared_key, server.public_key)
        m = "shared_key {}".format(binascii.hexlify(enc).decode('utf-8'))
        send_msg_to_server_async(server, m)

    # Generate and onion-encrypt messages
    messages = generate_chat_messages(num_messages)
    messages_enc = []
    for m in messages:
        print(m)
        messages_enc.append(onion_encrypt_message(m, servers))

    # Send onion-encrypted messages to the primary server
    # See server_skeleton script for the expected format of a messsage
    for m in messages_enc:
        send_msg_to_server_async(servers[0], "chat_msg_client {}".format(m.hex()))

    return messages


# Client which is responsible for making the PIR
# It should generate appropriate random masks for each server,
# send the pir requests and finally recover the target message
# Target message is the one with the provided target_msg_index
def client_receiver(servers, num_messages, target_msg_index):
    target_builder = ['0'] * num_messages
    target_builder[target_msg_index] = '1'
    bitmasks = [int(''.join(target_builder)[::-1], 2)]
    bitmasks += [int(''.join([random.choice('01') for _ in range(num_messages)]), 2) for _ in range(len(servers) - 1)]
    bitmasks.append(reduce(lambda x, y: x ^ y, bitmasks))
    responses = [send_msg_to_server(s, 'pir_req {}'.format(str(b))) for s, b in zip(servers, bitmasks[1:])]

    # Return the target message (string), only the body of the message,
    # without the message index
    return reduce(lambda x, y: bytes(i ^ j for i, j in zip(x, y)), responses).decode()


# This function is for your convenience, so you could test your solution locally
# Feel free to write your own test functions, this is just an example
def test_function():
    all_servers = read_server_data()

    messages = client_sender(all_servers, NUMBER_OF_CHAT_MSGS)

    print('Allow servers some time to exchange the messages')
    time.sleep(5)

    target_msg_index = random.randrange(NUMBER_OF_CHAT_MSGS)

    res = client_receiver(all_servers, NUMBER_OF_CHAT_MSGS, target_msg_index)

    for s in all_servers:
        send_msg_to_server_async(s, 'quit')

    target = messages[target_msg_index]

    if res == target[CHAT_MSG_INDEX_LEN:]:
        print('Success')
    else:
        print('Failure')


# This is the function which should be called when you upload your solution
# Your script will be provided with one cmd line argument, which is the index
# of the target message that you should recover with PIR
# Don't change this function!
def grading_main():
    if len(sys.argv) != 2:
        print('Wrong number of commmand line arguments')
    else:
        target_index = int(sys.argv[1])
        all_servers = read_server_data()
        result = client_receiver(all_servers, NUMBER_OF_CHAT_MSGS, target_index)
        print(result)


if __name__ == '__main__':
    # Feel free to replace the function and insert your own tests here
    # while you test your solution localy,
    # but when you want to upload your script for grading,
    # make sure this is the function which is called here!
    if len(sys.argv) == 2:
        grading_main()
    else:
        test_function()
