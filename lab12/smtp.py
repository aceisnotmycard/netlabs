import base64
import socket
import ssl

BUFFER_SIZE = 1024


class SMTPClient:
    s = None
    server = ""

    def __init__(self):
        pass

    def connect(self, server: str, ssl_enabled: bool) -> None:
        """
        :param server: target SMTP server
        :param ssl_enabled: if True then socket will be wrapped with ssl and port 465 will be used
        :return:
        """
        self.server = server
        self.s = socket.socket()
        if ssl_enabled:
            self.s = ssl.wrap_socket(self.s)
            self.s.connect((self.server, 465))
        else:
            self.s.connect((self.server, 25))
        self._check_response_code(220, "Cannot connect to target server")

        self._send('ehlo ' + self.server)
        self._check_response_code(250)
        print(self.server + ": connection established")

    def login(self, login: str, password: str) -> None:
        self._send("auth login")
        self._check_response_code(334)
        self._send(base64.b64encode(login.encode()).decode())
        self._check_response_code(334)
        self._send(base64.b64encode(password.encode()).decode())
        self._check_response_code(235)
        print(self.server + ": authentication complete")

    def set_header(self, author: str, recipient, subject: str) -> None:
        self._send("mail from:<{}>".format(author))
        self._check_response_code(250)
        self._send("rcpt to:<{}>".format(recipient))
        self._check_response_code(250)
        self._send("data")
        self._check_response_code(354)
        self._send("From: " + author)
        self._send("To: " + recipient)
        self._send("Subject: " + subject)
        self._send("")

    def set_content(self, content: [str]) -> None:
        for line in content:
            self._send(line)

    def end_message(self):
        self._send('.')
        self._check_response_code(250)
        print("Message sent successfully")

    def quit(self) -> None:
        self._send("quit")
        self._check_response_code(221)
        self.s.close()

    def _check_response_code(self, code: int, error_message="") -> bool:
        """
        :param code: expected code from server
        :param error_message: message that will be displayed if server return wrong code
        :return: True if code is returned
        """
        response = self.s.recv(BUFFER_SIZE).decode()
        if not response.startswith(str(code)):
            print("ERROR: " + error_message)
            self.s.close()
            quit()

    def _send(self, s: str) -> None:
        self.s.send((s + "\r\n").encode())
