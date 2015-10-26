import socket
import argparse
import os
import struct

BUFFER_SIZE = 1024
ENCODING = "utf8"
MSG_FILE_EXISTS = '0'
MSG_FILE_NOT_EXISTS = '1'

UPLOAD_DIR = 'uploads/'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive files from clients")
    parser.add_argument('port', type=int, help='Port to listen to', metavar='Port')
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', args.port))
    sock.listen(1)

    conn, addr = sock.accept()
    print('Connection address: {0}'.format(addr))
    data = conn.recv(BUFFER_SIZE)
    filename_size = struct.unpack('!H', data[:2])
    filename = str(data[2:], ENCODING)
    file = open(UPLOAD_DIR + filename, 'wb+')
    data = conn.recv(BUFFER_SIZE)
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        file.write(data)
    file.close()
    conn.send(struct.pack('!b', 0))
    conn.close()
