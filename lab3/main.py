import socket
import sys
import atexit

SOCK = None
PORT = 0
BROADCAST_ADDR = '255.255.255.255'
BORN_MSG = "IBORN"
LIVE_MSG = "ILIVE"
EXIT_MSG = "IEXIT"

hosts = set()


def send_msg(message: str, addr):
    SOCK.sendto(message.encode("utf8"), addr)


def list_hosts(hosts: set):
    print("List of alive hosts")
    for host in hosts:
        print(host)


@atexit.register
def say_goodbye():
    send_msg(EXIT_MSG, (BROADCAST_ADDR, PORT))


if __name__ == "__main__":
    PORT = int(sys.argv[-1])
    SOCK = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    send_msg(BORN_MSG, (BROADCAST_ADDR, PORT))
    while True:
        data, addr = SOCK.recvfrom(1024)
        if data.decode("utf8") == BORN_MSG:
            # add host to list, display it and say hello
            hosts.add(addr)
            list_hosts(hosts)
            send_msg(LIVE_MSG, addr)
        elif data.decode("utf8") == LIVE_MSG:
            # add host to list, display it
            hosts.add(addr)
            list_hosts(hosts)
        elif data.decode("utf8") == EXIT_MSG:
            # remove host from list and display list again
            if addr in hosts:
                hosts.remove(addr)
            list_hosts(hosts)
        else:
            # junk processing
            pass
