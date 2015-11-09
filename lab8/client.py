import socket
import struct
import sys
import threading
from lab8 import protocol

BUFFER_SIZE = 1024

HELP = """
Welcome!
h – show this menu
l – list available stations and current songs
{station number} – connect to specified station
d – disconnect from station
? – show current songs
"""


def listener(sock: socket.socket):
    while True:
        data = sock.recv(1024)
        print("Received: ", data.decode("utf8"))


def main(host: str, port: int):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((host, port))

    udp_thread = None

    print(HELP)
    while True:
        ch = input()
        if ch == "l":
            tcp_sock.send(protocol.get_stations())
            data = tcp_sock.recv(BUFFER_SIZE)
            if protocol.parse_type(data) == protocol.MSG_LIST:
                print(protocol.parse_text(data).decode())
        elif ch == "h":
            print(HELP)
        elif str.isdigit(ch):
            station_number = int(ch)
            tcp_sock.send(protocol.connect_to_station(station_number))
            data = tcp_sock.recv(BUFFER_SIZE)
            if protocol.parse_type(data) == protocol.MSG_CONNECT:
                group = protocol.parse_text(data).decode('utf8')
                udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_sock.bind(('', port))
                udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                mreq = struct.pack("=4sl", socket.inet_aton(group), socket.INADDR_ANY)
                udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                udp_thread = threading.Thread(target=listener, args=(udp_sock,))
                udp_thread.start()
        elif ch == "?":
            pass
        elif ch == "d":
            udp_sock.close()
            # stop listening to station
            pass
        else:
            print(HELP)


if __name__ == '__main__':
    main(sys.argv[-2], int(sys.argv[-1]))
