import sys
import signal
import socket
import struct
import threading

# protocol
FORMAT = '!bBBBBh'
CHILD = 0
MSG = 1
LEFT = 2
PARENT = 3
ROOT = 4

# technical
port = 3000
sock = None

# social
root = False
parent = None
children = []
me = None


def convert_ip_to_ints(ip: str):
    return [int(part) for part in ip.split('.')]


def create_message(msg_type: int, host: str, port: int) -> bytes:
    ints = convert_ip_to_ints(host)
    return struct.pack(FORMAT, msg_type, ints[0], ints[1], ints[2], ints[3], port)


# handling ctrl-c
def exit_handler(arg1, arg2):
    if len(children) > 0:
        if root:
            new_parent = children[0]
            sock.sendto(create_message(ROOT, me[0], me[1]), new_parent)
        else:
            new_parent = parent
            sock.sendto(create_message(LEFT, me[0], me[1]), parent)
        for child in children:
            if child != new_parent:
                sock.sendto(create_message(PARENT, new_parent[0], new_parent[1]), child)
    sys.exit(0)


def reader():
    while True:
        msg_body = str(input()).encode("utf8")
        msg_header = create_message(MSG, me[0], me[1])
        if not root:
            sock.sendto(msg_header + msg_body, parent)
        for child in children:
            sock.sendto(msg_header + msg_body, child)


if __name__ == "__main__":

    # Parse arguments
    port = int(sys.argv[1])
    root = True
    if len(sys.argv) == 4:
        parent = (sys.argv[-2], int(sys.argv[-1]))
        root = False

    # Register exit handler
    signal.signal(signal.SIGINT, exit_handler)

    # Socket configuration
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.bind(('', port))
    me = (socket.gethostbyname(socket.gethostname()), port)

    thread = threading.Thread(target=reader)
    thread.start()

    # Notify parent
    if not root:
        sock.sendto(create_message(CHILD, me[0], me[1]), parent)
        print("Sending hello to parent")

    while True:
        received, addr = sock.recvfrom(1024)
        data = received[:7]
        recv = struct.unpack(FORMAT, data)
        type = recv[0]
        recv_ip = "{0}.{1}.{2}.{3}".format(recv[1], recv[2], recv[3], recv[4])
        recv_port = recv[5]
        # we've got new child
        if type == CHILD:
            children.append((recv_ip, recv_port))
            print("New child at {0}:{1}".format(recv_ip, recv_port))
        # message received
        elif type == MSG:
            print("Message from {0}:{1}: {2}".format(recv_ip, recv_port, str(received[7:].decode("utf8"))))
            if addr == parent:
                for child in children:
                    sock.sendto(data, child)
            else:
                for child in children:
                    if child != addr:
                        sock.sendto(data, child)
                if not root:
                    sock.sendto(data, parent)
        # someone is left
        elif type == LEFT:
            if (recv_ip, recv_port) in children:
                children.remove((recv_ip, recv_port))
                print("Child removed")
        # he is my new parent
        elif type == PARENT:
            parent = (recv_ip, recv_port)
            print("New parent at {0}:{1}".format(recv_ip, recv_port))
        # i'm the king, baby
        elif type == ROOT:
            root = True
            parent = None
            print("I'm gROOT")
        else:
            print("WOW WAT NO WAY")
