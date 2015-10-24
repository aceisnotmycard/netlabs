import socket
import argparse
from hashlib import md5


sequences = []
iter = 0


def create_ranges(genome_len: int, num_ranges: int):
    if num_ranges == 1:
        sequences.append("a" * genome_len)
    else:
        trigger = 4**genome_len // (num_ranges-1)
        generator(length=genome_len, trigger=trigger)

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


def generator(length=4, seq="", trigger: int = 1):
    global sequences
    global iter
    alph = ["a", "c", "g", "t"]
    if length == 0:
        if iter % trigger == 0:
            sequences.append(seq)
    else:
        for a in alph:
            generator(length - 1, seq + a, trigger=trigger)
            iter += 1


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Cracks given genome")
    # parser.add_argument('genome', type=str, help='Genome to crack', metavar='Genome')
    # parser.add_argument('port', type=int, help='Port to listen to', metavar='Port')
    # args = parser.parse_args()
    # main(args.genome, args.port)
    create_ranges(genome_len=2, num_ranges=8)
    for s in sequences:
        print(s)
