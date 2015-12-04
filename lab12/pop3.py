import socket
import ssl
import struct

BUFFER_SIZE = 1024


class POP3Client:
    s = None
    server = ""
    count = 0

    def __init__(self):
        pass

    def connect(self, server: str, is_ssl_enabled: bool) -> None:
        self.server = server
        self.s = socket.socket()
        if is_ssl_enabled:
            self.s = ssl.wrap_socket(self.s)
            self.s.connect((server, 995))
        else:
            self.s.connect(110)
        self._check()
        print(self.server + ": connection established")

    def login(self, login: str, password: str):
        self._send("user " + login)
        self._check()
        self._send("pass " + password)
        self._check()
        print(self.server + ": authentication complete")

    def list(self):
        self._send("stat")
        self.count = int(self._check().split(sep=" ")[1])
        for i in range(1, self.count + 1):
            self.show_header_for(i)

    def show_header_for(self, msg_pos: int):
        self._send("top {0} {1}".format(msg_pos, 0))
        subject = ""
        author = ""
        while True:
            t = self.s.recv(BUFFER_SIZE).decode('utf-8')
            if t.startswith("Subject"):
                subject = t[len("Subject:"):]
            if t.startswith("From: "):
                author = t[:-1]
            if t == '.\n' or t == '.\r\n':
                break
        row = (subject + " " + author).replace("\r\n", " ")
        print(msg_pos, row)

    def show_message(self, msg_pos: int):
        if msg_pos > self.count:
            print("There are only {} messages!".format(self.count))
            return
        self._send("retr {}".format(msg_pos))
        while True:
            t = self.s.recv(BUFFER_SIZE)
            if t == b"\r\n.\r\n":
                break
            print(t.decode('utf-8'))

    def stat(self):
        self._send("stat")
        content = self._check()
        print(content)

    def quit(self) -> None:
        self.s.close()

    def _check(self, ) -> str:
        response = self.s.recv(BUFFER_SIZE).decode()
        if not response.startswith("+OK"):
            print("FAIL: " + response)
            self.s.close()
            quit()
        return response

    def _send(self, msg: str):
        self.s.write((msg + "\n").encode())
