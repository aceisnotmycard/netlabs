import sys
import threading
import time
import socketserver
from os import listdir
from os.path import isfile, join

from lab8 import protocol

BUFFER_SIZE = 1024


class Station:
    def __init__(self, folder: str):
        self.songs = [f for f in listdir(folder) if isfile(join(folder, f))]

    def run(self):
        for f in self.songs:
            print("Opening {}".format(f))
            time.sleep(1)
            with open(f, 'r') as song:
                for line in song.readlines():
                    print(line)
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
                self.request.sendall(protocol.send_stations(b"A net tvoih pesen ahahaha"))
            elif msg_type == protocol.MSG_CONNECT:
                station_number = protocol.parse_station(data)
                print("{0} now listening station #{1}".format(self.client_address, station_number))
            elif msg_type == protocol.MSG_DISCONNECT:
                print("{0} disconnected from station".format(self.client_address))
            else:
                print("WTF?")


def main(port: int):
    server = socketserver.ThreadingTCPServer(('', port), MusicTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()


if __name__ == '__main__':
    main(int(sys.argv[-1]))
