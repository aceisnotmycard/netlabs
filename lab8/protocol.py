import struct

# show menu
MSG_HELP = 0
# list stations
MSG_LIST = 1
# what is playing on current station?
MSG_SONG = 2
# connect to specified station
MSG_CONNECT = 3
# disconnect from current station
MSG_DISCONNECT = 4
# client disconnected
MSG_EXIT = 5


def send_stations(stations: str):
    return struct.pack("!bi{}s".format(len(stations)), MSG_LIST, len(stations), stations.encode('utf8'))


def send_addr(addr: str):
    return struct.pack("!bi{}s".format(len(addr)), MSG_CONNECT, len(addr), addr.encode('utf8'))


def get_stations():
    return struct.pack("!b", MSG_LIST)


def exit():
    return struct.pack("!b", MSG_EXIT)


def connect_to_station(station: int):
    return struct.pack("!bi", MSG_CONNECT, station)


def parse_text(data: bytes):
    length = struct.unpack("!i", data[1:5])[0]
    return struct.unpack("!{}s".format(length), data[5:])[0]


def parse_station(data: bytes):
    return struct.unpack("!i", data[1:5])[0]


def parse_type(data: bytes):
    return struct.unpack("!b", data[:1])[0]
