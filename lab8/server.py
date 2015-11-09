import socket
import sys
import threading
import time
import socketserver
from os import listdir
from os.path import isfile, join

from lab8 import protocol

BUFFER_SIZE = 1024

MULTICAST_BASE = '239.255.0.'

stations = {}


class Station(threading.Thread):
    def __init__(self, folder: str, mcast):
        super(Station, self).__init__()
        self.folder = folder
        self.songs = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.mcast = mcast
        self.current_song = ""

    def run(self):
        super(Station, self).run()
        while True:
            for f in self.songs:
                # print("Opening {}".format(f))
                time.sleep(1)
                self.current_song = f
                with open(self.folder + '/' + f, 'rb') as song:
                    data = song.read(BUFFER_SIZE)
                    while data:
                        self.sock.sendto(data, self.mcast)
                        data = song.read(BUFFER_SIZE)
                        time.sleep(1)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class MusicTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(BUFFER_SIZE)
            msg_type = protocol.parse_type(data)
            if msg_type == protocol.MSG_LIST:
                print("{0} required stations list".format(self.client_address))
                msg = ""
                for k in stations:
                    msg += "{0}. {1}".format(k, stations[k].current_song) + "\n"
                self.request.sendall(protocol.send_stations(msg))
            elif msg_type == protocol.MSG_CONNECT:
                station_number = protocol.parse_station(data)
                print("{0} now listening station #{1}".format(self.client_address, station_number))
                self.request.sendall(protocol.send_addr(stations[station_number].mcast[0]))
            elif msg_type == protocol.MSG_DISCONNECT:
                print("{0} disconnected from station".format(self.client_address))
            elif msg_type == protocol.MSG_EXIT:
                print("Client {} disconnected".format(self.client_address))
                return
            else:
                print("WTF?")


def main(port: int):
    for i in range(0, 4):
        stations[i] = Station('radio{}'.format(i), (MULTICAST_BASE + str(i), port))
        stations[i].start()

    server = socketserver.ThreadingTCPServer(('', port), MusicTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()


if __name__ == '__main__':
    main(int(sys.argv[-1]))
