import socket
import sys

BUFER_SIZE = 1024

if __name__ == "__main__":
    filename = sys.argv[-1]
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket()
    s.connect((host, port))
    s.send("hello".encode("utf8"))
