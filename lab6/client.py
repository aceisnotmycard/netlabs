from hashlib import md5


def str_to_md5(genome: str):
    md5(bytes(genome, "utf8")).digest()


def is_cracked(candidate: str, encrypted_genome: str) -> bool:
    return str_to_md5(candidate) == encrypted_genome


if __name__ == '__main__':

