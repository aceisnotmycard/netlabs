import signal
import socket
import sys
import atexit

sock = None
hosts = set()

PORT = 0
BROADCAST_ADDR = '255.255.255.255'
BORN_MSG = "IBORN"
LIVE_MSG = "ILIVE"
EXIT_MSG = "IEXIT"


def send_msg(message: str, addr):
    print("Sending {0} to {1}".format(message, addr))
    sock.sendto(message.encode("utf8"), addr)


def list_hosts(hosts: set):
    print("List of alive hosts")
    for host in hosts:
        print(host)


# handling ctrl-c
def exit_handler(signum, frame):
    print("Ok, exit :(")
    sys.exit(0)


@atexit.register
def say_goodbye():
    send_msg(EXIT_MSG, (BROADCAST_ADDR, PORT))


if __name__ == "__main__":
    # register signal handler
    signal.signal(signal.SIGINT, exit_handler)

    PORT = int(sys.argv[-1])
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', PORT))

    send_msg(BORN_MSG, (BROADCAST_ADDR, PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        recv_msg = data.decode("utf8")
        print("Received {0} from {1}".format(recv_msg, addr))
        if recv_msg == BORN_MSG:
            # add host to list, display it and say hello
            hosts.add(addr)
            list_hosts(hosts)
            send_msg(LIVE_MSG, addr)
        elif recv_msg == LIVE_MSG:
            # add host to list, display it
            hosts.add(addr)
            list_hosts(hosts)
        elif recv_msg == EXIT_MSG:
            # remove host from list and display list again
            if addr in hosts:
                hosts.remove(addr)
            list_hosts(hosts)
        else:
            # junk processing
            print("Received junk")
