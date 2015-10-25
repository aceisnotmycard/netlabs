import struct

# client messages
START_CRACK = "0"
TAKE_MORE = "1"
SUCCESS = "2"

# server messages
GIVE_GENOME = "0"
GIVE_MORE = "1"
NO_MORE = "2"


def start_crack():
    return struct.pack("!cis", START_CRACK, 0, "")


def take_more():
    return struct.pack("!cis", TAKE_MORE, 0, "")


def success(genome: str):
    return struct.pack("!cis", SUCCESS, len(genome), genome)


def give_genome(encrypted_genome: str, genome_len: int):
    return struct.pack("!cis", GIVE_GENOME, genome_len, encrypted_genome)


def give_more(seq: (str, int)):
    return struct.pack("!cis", GIVE_MORE, seq[0], seq[1])


def no_more():
    return struct.pack("!cis", NO_MORE, 0, "")


def read(msg):
    return struct.unpack("!cis", msg)