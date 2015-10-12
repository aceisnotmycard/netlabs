__author__ = 'sergey'
import socket
import sys


BUFFER_SIZE = 1024


"""
Protocol:
1) filename size
2) filename
3) file size
4) file
"""
if __name__ == "__main__":
    port = int(sys.argv[1])
    s = socket.socket()
    s.bind(("", port))
    s.listen(1)

    while True:
        sc, address = s.accept()
        print(address)
        print(sc)