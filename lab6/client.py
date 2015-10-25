import argparse
from hashlib import md5
import socket
from lab6 import proto


def str_to_md5(genome: str):
    return md5(genome.encode("utf8")).digest()


def cracked(candidate: str, encrypted_genome: str) -> bool:
    return str_to_md5(candidate) == encrypted_genome


def get_next_seq(seq: str, pos) -> str:
    if pos > len(seq):
        return seq
    if seq[-pos] == "a":
        return seq[:-pos] + "c" + "a" * (pos - 1)
    elif seq[-pos] == "c":
        return seq[:-pos] + "g" + "a" * (pos - 1)
    elif seq[-pos] == "g":
        return seq[:-pos] + "t" + "a" * (pos - 1)
    elif seq[-pos] == "t":
        seq = seq[:-pos] + 'a' * pos
        return get_next_seq(seq, pos + 1)


def crack(seq: str, count: int, encrypted_genome: str) -> (str, bool):
    for i in range(count):
        if not cracked(seq, encrypted_genome):
            seq = get_next_seq(seq, 1)
        else:
            return seq, True
    else:
        return "", False


def main(server: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    sock.send(proto.start_crack())
    data = sock.recv(1024)
    type, size, msg = proto.read(data)
    if type == proto.GIVE_GENOME:
        print(msg.decode(encoding='utf8'))
    else:
        print("Fail")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cracks given genome")
    parser.add_argument('server', type=str, help='Server', metavar='Server')
    parser.add_argument('port', type=int, help='Port', metavar='Port')
    args = parser.parse_args()
    main(args.server, args.port)