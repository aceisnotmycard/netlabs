import signal
import socket
import struct
import sys
import threading
import pyaudio
from lab8 import protocol

BUFFER_SIZE = 1024

HELP = """
Welcome!
h – show this menu
l – list available stations and current songs
{station number} – connect to specified station
d – disconnect from station
"""


# todo
def audio_listener(sock: socket.socket):
    p = pyaudio.PyAudio()
    stream = p.open(output=True)
    while True:
        try:
            data = sock.recv(1024)
            # print("Received: ", data)
        except OSError:
            return


def listener(sock: socket.socket):
    while True:
        try:
            data = sock.recv(1024)
            print("Received: ", data)
        except OSError:
            return


def main(host: str, port: int):
    tcp_sock = None
    udp_thread = None
    udp_sock = None

    def exit_handler(arg1, arg2):
        tcp_sock.send(protocol.exit())
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_handler)

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((host, port))

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
                udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                udp_sock.bind(('', port))
                mreq = struct.pack("=4sl", socket.inet_aton(group), socket.INADDR_ANY)
                udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                udp_thread = threading.Thread(target=listener, args=(udp_sock,))
                udp_thread.daemon = True
                udp_thread.start()
        elif ch == "d":
            print('Disconnected from station')
            udp_sock.close()
            # stop listening to station
            pass
        else:
            print(HELP)


if __name__ == '__main__':
    main(sys.argv[-2], int(sys.argv[-1]))
