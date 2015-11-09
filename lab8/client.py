import socket
import sys

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


def main(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(HELP)
    while True:
        ch = input()
        if ch == "l":
            sock.send(protocol.get_stations())
            data = sock.recv(BUFFER_SIZE)
            if protocol.parse_type(data) == protocol.MSG_LIST:
                print(protocol.parse_text(data))
        elif ch == "h":
            print(HELP)
        elif str.isdigit(ch):
            station_number = int(ch)
            sock.send(protocol.connect_to_station(station_number))
        elif ch == "?":
            pass
        elif ch == "d":
            pass
        else:
            print(HELP)


if __name__ == '__main__':
    main(sys.argv[-2], int(sys.argv[-1]))
