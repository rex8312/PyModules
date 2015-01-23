__author__ = 'rex8312'

from gevent import socket
from gevent import monkey
monkey.patch_all()


if __name__ == '__main__':
    address = ('127.0.0.1', 8888)
    sock = socket.socket(type=socket.SOCK_STREAM)
    sock.connect(address)

    fp = sock.makefile()
    while True:
        message = raw_input()
        message += '\n'
        fp.write(message)
        fp.flush()
        line = fp.readline()
        line = line.strip()
        print line

    sock.close()