# -*-coding: utf-8 -*-

__author__ = 'rex8312'

"""
gevent를 이용한 기본 TCP 서버
"""


from gevent import socket
from gevent.server import StreamServer
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()


class EchoServer(StreamServer):

    def handle(self, sock, address):
        fp = sock.makefile()
        print '_'
        line = fp.readline()
        print 'read'
        print line.strip()
        fp.write(line.upper() + '\n')
        print 'send'
        fp.flush()


if __name__ == '__main__':
    pool = Pool(10000)
    server = EchoServer(('127.0.0.1', 8888), spawn=pool)
    server.serve_forever()
