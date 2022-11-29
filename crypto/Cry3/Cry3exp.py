import itertools
import string
from hashlib import sha256
import gmpy2
from Crypto.Util.number import long_to_bytes
from pwn import remote, context, xor
from Crypto.Util.Padding import pad

# context.log_level = 'debug'


def Proof(broke, Hash):
    assert len(broke) == 16 and len(Hash) == 64
    shaTable = string.ascii_letters + string.digits
    for ii in itertools.permutations(shaTable, 4):
        x = ''.join(ii)
        s = x + broke
        if sha256(s.encode()).hexdigest() == Hash:
            return x


def exgcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = exgcd(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, gcd


def cbcMAC():
    p = remote("120.78.131.38", 10010)
    data1 = p.recvuntil(b'Give Me XXXX:\n')
    x = (Proof(data1[14:30].decode(), data1[32:96].decode())).encode()
    p.sendline(x)
    data2 = p.recvuntil(b'--> ').decode()
    mac = data2.strip()[-36:-4]
    msg = 'Whitfield__Diffie'
    b1, b2 = msg[:16].encode(), msg[16:].encode()  # first block
    msg = pad(msg.encode(), 16)
    sMen = msg + xor(bytes.fromhex(mac), b1) + b2
    p.send(sMen)
    p.recvuntil(b'penetrated.\n')
    c = p.recvuntil(b')')
    return c[34:]


def sameMod():
    c = cbcMAC().decode()[1:-1].split(', ')
    cipher = [int(i) for i in c]
    n, e1, e2, e3, c1, c2, c3 = cipher[0], cipher[1], cipher[2], cipher[3], cipher[4], cipher[5], cipher[6]
    a = gmpy2.gcd(e1, e2)
    b = gmpy2.gcd(e1, e3)
    c = gmpy2.gcd(e2, e3)

    x1 = exgcd(b, c)
    C1 = gmpy2.powmod(c1, x1[0], n) * gmpy2.powmod(c2, x1[1], n) % n

    x2 = exgcd(a, b)
    C2 = gmpy2.powmod(c2, x2[0], n) * gmpy2.powmod(c3, x2[1], n) % n

    x3 = exgcd(a, c)
    flag = gmpy2.powmod(C1, x3[0], n) * gmpy2.powmod(C2, x3[1], n) % n
    print(long_to_bytes(flag))


if __name__ == '__main__':
    sameMod()
