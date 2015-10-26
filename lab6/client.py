import argparse
from hashlib import md5
import socket
from lab6 import proto


def cracked(candidate: str, encrypted_genome: str) -> bool:
    return md5(candidate.encode("utf8")).digest() == encrypted_genome


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
            print(seq)
            seq = get_next_seq(seq, 1)
        else:
            return seq, True
    else:
        return "", False


def try_crack(data: bytes, genome: str) -> (str, bool):
    if proto.parse_msg_type(data) == proto.NO_MORE:
        print("No more sequences. Soryan")
        exit(0)  # todo: refactor
    steps, seq = proto.parse_more(data)
    return crack(seq, steps, genome)


def send_msg(server, port, msg: bytes):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    sock.send(msg)
    response = sock.recv(1024)
    sock.close()
    return response


def main(server: str, port: int):
    data = send_msg(server, port, proto.start_crack())
    msg_type = proto.parse_msg_type(data)
    if msg_type == proto.GIVE_GENOME:
        genome = proto.parse_genome(data)
        data = send_msg(server, port, proto.take_more())
        seq, success = try_crack(data, genome)
        while not success:
            data = send_msg(server, port, proto.take_more())
            seq, success = try_crack(data, genome)
        else:
            send_msg(server, port, proto.success(seq))
            print(seq)
    else:
        print("Fail")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Cracks given genome")
    parser.add_argument('server', type=str, help='Server', metavar='Server')
    parser.add_argument('port', type=int, help='Port', metavar='Port')
    args = parser.parse_args()
    main(args.server, args.port)
