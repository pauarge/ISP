import asyncio
import websockets
import binascii
import random
import hashlib

email = "pau.argelaguet@epfl.ch"
password = "PgQDSxNSFAACBUcURRw1CBEITFoMSA=="
n = "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
N = int(n, 16)
g = 2


def parse_number(raw):
    buff = binascii.unhexlify(raw)
    return int.from_bytes(buff, 'big')


def H(a):
    return int(hashlib.sha256(a).hexdigest(), 16)


async def hello():
    async with websockets.connect('ws://com402.epfl.ch/hw2/ws') as websocket:
        print("-> U: {}".format(email))
        await websocket.send(email.encode('utf-8'))

        x = await websocket.recv()
        salt = parse_number(x)
        SB = salt.to_bytes((salt.bit_length() + 7) // 8, 'big')
        print("<- salt: {}".format(salt))

        a = random.SystemRandom().getrandbits(32)
        A = pow(g, a, N)
        print("-> A: {}".format(A))
        AB = A.to_bytes((A.bit_length() + 7) // 8, 'big')
        await websocket.send(binascii.hexlify(AB).decode())

        x = await websocket.recv()
        B = parse_number(x)
        BB = B.to_bytes((B.bit_length() + 7) // 8, 'big')
        print("<- B: {}".format(B))

        u = H(AB + BB)
        print("u: {}".format(u))

        up = H("{}:{}".format(email, password).encode('utf-8'))
        upB = up.to_bytes((up.bit_length() + 7) // 8, 'big')
        x = H(SB + upB)
        print("x: {}".format(x))

        S = pow(B - pow(g, x, N), a + u * x, N)
        SB = S.to_bytes((S.bit_length() + 7) // 8, 'big')
        print("S: {}".format(S))

        habs = H(AB + BB + SB)
        print("-> H(A||B||S): {}".format(habs))
        buff = habs.to_bytes((habs.bit_length() + 7) // 8, 'big')
        await websocket.send(binascii.hexlify(buff).decode())

        res = await websocket.recv()
        print(res)


asyncio.get_event_loop().run_until_complete(hello())
