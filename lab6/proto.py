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
    return struct.pack("!bi{0}s".format(len(genome.encode("utf8"))), SUCCESS, len(genome), genome.encode("utf8"))


def give_genome(encrypted_genome: bytes, genome_len: int):
    return struct.pack("!bi{0}s".format(len(encrypted_genome)), GIVE_GENOME, genome_len, encrypted_genome)


def give_more(seq: (str, int)):
    return struct.pack("!bi{0}s".format(len(seq[1].encode("utf8"))), GIVE_MORE, seq[0], seq[1].encode("utf8"))


def no_more():
    return struct.pack("!bis", NO_MORE, 0, "".encode("utf8"))


def read(msg):
    return struct.unpack("!bis", msg)