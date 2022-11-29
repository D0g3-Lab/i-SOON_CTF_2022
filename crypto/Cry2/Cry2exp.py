# -*- coding:utf-8 -*-
from pwn import *
import string
from hashlib import sha256
from Crypto.Cipher import AES
import itertools
# context.log_level = 'debug'


def decrypt(key, message):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(message)


def Proof(broke, Hash):
    assert len(broke) == 16 and len(Hash) == 64
    shaTable = string.ascii_letters + string.digits
    for ii in itertools.permutations(shaTable, 4):
        x = ''.join(ii)
        s = x + broke
        if sha256(s.encode()).hexdigest() == Hash:
            return x


def main():
    table = string.ascii_letters + string.digits
    r = remote('120.78.131.38', 10086)
    data1 = r.recvuntil(b'Give Me XXXX:\n')
    print(data1)
    flag1, flag2 = b'', b''
    x = (Proof(data1[14:30].decode(), data1[32:96].decode())).encode()
    r.sendline(x)
    for i in range(23, 3, -1):
        r.recv()
        sendMessage = b'*' * i
        r.sendline(sendMessage)
        a = r.recv()
        ecbCipher = str(a)[25:-4][32:64]
        flag1 = a[23:-2]
        for guess in table:
            r.recv()
            r.sendline(sendMessage + flag2 + guess.encode())
            b = r.recv()
            if str(b)[25:-2][32:64] == ecbCipher:
                flag2 += guess.encode()
                break
        if len(flag2) == 15:
            break
    print(flag2)
    flag2 = flag2 + b'}'
    flag1 = decrypt(flag2, binascii.unhexlify(flag1))
    print(flag1[:8]+flag2)


if __name__ == '__main__':
    main()