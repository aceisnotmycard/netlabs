from hashlib import md5


def str_to_md5(genome: str):
    md5(bytes(genome, "utf8")).digest()


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


def crack(seq: str, count: int, encrypted_genome: str):
    for i in range(count):
        if not cracked(seq, encrypted_genome):
            seq = get_next_seq(seq)
            print(seq)
        else:
            return seq



if __name__ == '__main__':
    crack("aaa", 16, "")
