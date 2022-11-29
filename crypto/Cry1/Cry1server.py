# -*- coding:utf-8 -*-
import os
import random
import string
import hashlib
import socketserver

flag = 'D0g3{Y0u_C4n_gu3ss_The_Fl4g}'


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

    def handle(self):
        if not self.proof():
            self.request.sendall(b'Error Hash!')
            return

        self.request.sendall('If you guessed right, I\'ll give you the flag!, You only have 6 chances (1~20)\n'.encode())
        number = str(random.randint(1, 20))
        n = 0
        while n < 6:
            guess = self.request.recv(512).strip().decode()
            if guess != number:
                self.request.sendall('wrong number, guess again:\n'.encode())
            else:
                self.request.sendall(('right!, give you flag: %s' % flag).encode())
                return
            n += 1
        self.request.sendall('See you next time!\n'.encode())
        return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    sever = socketserver.ThreadingTCPServer(('0.0.0.0', 10001), MyServer)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    sever.serve_forever()
