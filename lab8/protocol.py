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


def send_stations(stations: bytes):
    return struct.pack("!bi{}s".format(len(stations)), MSG_LIST, len(stations), stations)


def get_stations():
    return struct.pack("!b", MSG_LIST)


def connect_to_station(station: int):
    return struct.pack("!bi", MSG_CONNECT, station)

def parse_text(data: bytes):
    length = struct.unpack("!i", data[1:5])[0]
    return struct.unpack("!{}s".format(length), data[5:])[0]


def parse_station(data: bytes):
    return struct.unpack("!i", data[1:5])[0]


def parse_type(data: bytes):
    return struct.unpack("!b", data[:1])[0]
