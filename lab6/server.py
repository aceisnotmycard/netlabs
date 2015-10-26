import socket
import argparse
from hashlib import md5
import math
from lab6 import proto

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
    encrypted_genome = md5(genome.encode("utf8")).digest()
    sequences = create_ranges(genome_len=len(genome), num_ranges=8)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        msg_type = proto.parse_msg_type(data)
        if msg_type == proto.START_CRACK:
            conn.send(proto.give_genome(encrypted_genome))
        elif msg_type == proto.TAKE_MORE:
            for seq in sequences:
                if not seq:
                    conn.send(proto.give_more(seq))
                    seq = True
                    clients_list[addr] = seq
                    for client, val in clients_list:
                        print(client, val)
                    break
            else:
                conn.send(proto.no_more())
        elif msg_type == proto.SUCCESS:
            # parse data and close other connections
            print("{0} found answer: {1} ".format(addr, proto.parse_success(data)))
            conn.send(1)
        conn.close()







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cracks given genome")
    parser.add_argument('genome', type=str, help='Genome to crack', metavar='Genome')
    parser.add_argument('port', type=int, help='Port to listen to', metavar='Port')
    args = parser.parse_args()
    main(args.genome, args.port)