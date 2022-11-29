import binascii
import hashlib
import os
import random
import socketserver
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import getPrime, bytes_to_long

hint = ''
flag = b''
key = os.urandom(16)

GOD = [b'Whitfield__Diffie']


def encrypt(message):
    message = pad(message, 16)
    aes = AES.new(key, AES.MODE_CBC, iv=b'\x00' * AES.block_size)
    return binascii.hexlify(aes.encrypt(message)[-16:])


Authentication = encrypt(b'Whitfield__Diffie')


class CryptoPalace(socketserver.StreamRequestHandler):
    def proof1(self):
        random.seed(os.urandom(8))
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        str_sha256 = hashlib.sha256(random_str.encode()).hexdigest()
        self.request.sendall(('SHA256(XXXX + %s):%s\n' % (random_str[4:], str_sha256)).encode())
        self.request.sendall('Give Me XXXX:\n'.encode())
        XXXX = self.request.recv(2048).strip()
        if hashlib.sha256((XXXX + random_str[4:].encode())).hexdigest() != str_sha256:
            return False
        return True

    def proof2(self):
        self.request.sendall(b'You must prove your identity to enter the palace ' + Authentication + b'\n--> ')
        name = self.request.recv(1024)
        if name in GOD:
            self.request.sendall(b'\n You\'re not him! \n')
            return False
        if encrypt(name) != Authentication:
            self.request.sendall(b'\n Wrong, try again......\n')
            return False
        else:
            self.request.sendall(hint.encode() + b"\n")
            return True

    def DiffieEncrypt(self):
        p, q = getPrime(1024), getPrime(1024)
        E = [getPrime(512) for _ in range(3)]
        e1, e2, e3 = E[0] * E[1], E[0] * E[2], E[1] * E[2]
        n = p * q
        m = bytes_to_long(flag)
        c1, c2, c3 = pow(m, e1, p * q), pow(m, e2, p * q), pow(m, e3, p * q)
        return n, e1, e2, e3, c1, c2, c3

    def handle(self):
        if not self.proof1():
            self.request.sendall(b'Error Hash!')
            return

        if not self.proof2():
            self.request.sendall(b'You didn\'t enter the palace\n')
            return

        self.request.sendall(b'\nFlag has been encrypted by Diffie\n')
        cipher = self.DiffieEncrypt()
        self.request.sendall(str(cipher).encode())
        return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    host, port = '120.78.131.38', 10010
    server = ThreadedTCPServer((host, port), CryptoPalace)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    server.serve_forever()
