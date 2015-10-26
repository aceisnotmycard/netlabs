import struct

# client messages
START_CRACK = 0
TAKE_MORE = 1
SUCCESS = 3

# server messages
GIVE_GENOME = 0
GIVE_MORE = 1
NO_MORE = 2


def start_crack():
    return struct.pack("!bis", START_CRACK, 0, "".encode("utf8"))


def take_more():
    return struct.pack("!bis", TAKE_MORE, 0, "".encode("utf8"))


def success(genome: str):
    return struct.pack("!bi{}s".format(len(genome.encode("utf8"))), SUCCESS, len(genome), genome.encode("utf8"))


def give_genome(encrypted_genome: bytes):
    return struct.pack("!bi{}s".format(len(encrypted_genome)), GIVE_GENOME, len(encrypted_genome), encrypted_genome)


def give_more(seq: (str, int)):
    return struct.pack("!bii{}s".format(len(seq[0])), GIVE_GENOME, seq[1], len(seq[0]), seq[0].encode("utf8"))


def no_more():
    return struct.pack("!bis", NO_MORE, 0, "".encode("utf8"))


def read(msg):
    return struct.unpack("!bis", msg)


def parse_msg_type(data: bytes):
    return struct.unpack("!b", data[:1])[0]


def parse_genome(data: bytes):
    genome_len = struct.unpack("!i", data[1:5])[0]
    return struct.unpack("!{}s".format(genome_len), data[5:])[0]


def parse_more(data: bytes):
    steps = struct.unpack("!i", data[1:5])[0]
    seq_len = struct.unpack("!i", data[5:9])[0]
    seq = struct.unpack("!{}s".format(seq_len), data[9:])[0].decode("utf8")
    return steps, seq


def parse_success(data: bytes):
    genome_len = struct.unpack("!i", data[1:5])[0]
    return struct.unpack("!{}s".format(genome_len), data[5:])[0].decode("utf8")