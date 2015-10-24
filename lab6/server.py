import socket
import argparse
from hashlib import md5
import math

prev_seq = ""


def create_ranges(genome_len: int, num_ranges: int):
    sequences = {}
    offsets = [int]
    counter = [0]
    prev_counter = [0]

    # generating starting sequences
    def seq_gen(length=4, seq="", trigger: int = 1):
        acgt = ["a", "c", "g", "t"]
        global prev_seq
        if length == 0:
            if counter[0] == 0:
                prev_seq = seq
            elif seq == "t" * genome_len:
                sequences[(prev_seq, counter[0] - prev_counter[0] + 1)] = False
            elif counter[0] % trigger == 0:
                sequences[(prev_seq, counter[0] - prev_counter[0])] = False
                prev_seq = seq
                prev_counter[0] = counter[0]
            counter[0] += 1
        else:
            for c in acgt:
                seq_gen(length - 1, seq + c, trigger=trigger)

    trigger = math.ceil(4 ** genome_len / num_ranges)
    seq_gen(length=genome_len, trigger=trigger)
    return sequences


def main(genome: str, port: int):
    clients_list = []

    encrypted_genome = md5(genome).digest()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)


def printer(l, start=""):
    alph = ["a", "c", "g", "t"]
    if l == 0:
        # do something here
        pass
    else:
        for a in alph:
            printer(l - 1, start + a)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Cracks given genome")
    # parser.add_argument('genome', type=str, help='Genome to crack', metavar='Genome')
    # parser.add_argument('port', type=int, help='Port to listen to', metavar='Port')
    # args = parser.parse_args()
    # main(args.genome, args.port)
    sequences = create_ranges(genome_len=3, num_ranges=4)
    for k in sequences:
        print(k, sequences[k])
