# -*- coding:utf-8 -*-
import os
import random
import string
import hashlib
import binascii
import socketserver
from Crypto.Cipher import AES

flag = 'D0g3{AtkkSUKUMYeRf0wXFX}'


class MyServer(socketserver.BaseRequestHandler):
    def proof(self):
        random.seed(os.urandom(8))
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        str_sha256 = hashlib.sha256(random_str.encode()).hexdigest()
        self.request.sendall(('SHA256(XXXX + %s):%s\n' % (random_str[4:], str_sha256)).encode())
        self.request.sendall('Give Me XXXX:\n'.encode())
        XXXX = self.request.recv(2048).strip()

        if hashlib.sha256((XXXX + random_str[4:].encode())).hexdigest() != str_sha256:
            return False

        return True

    def pad(self, message):
        if len(message) % 16 != 0:
            return message.ljust((len(message) // 16 + 1) * 16, '0').encode()
        else:
            return message.encode()

    def encrypt(self, key, message):
        aes = AES.new(key, AES.MODE_ECB)
        return aes.encrypt(message)

    def decrypt(self, key, message):
        aes = AES.new(key, AES.MODE_ECB)
        return aes.decrypt(message)

    def handle(self):
        if not self.proof():
            self.request.sendall(b'Error Hash!')
            return

        flag1, flag2 = flag[:8], flag[8:]
        while 1:
            self.request.sendall('You can input anything:\n'.encode())
            iMessage = self.request.recv(2048).strip().decode()
            message = self.pad(flag1 + iMessage + flag2)
            cipher = binascii.hexlify(self.encrypt(flag2.encode(), message))
            self.request.sendall(('Here is your cipher: %s\n' % cipher).encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    sever = socketserver.ThreadingTCPServer(('0.0.0.0', 10086), MyServer)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    sever.serve_forever()
