import sys

from lab11.smtp import SMTPClient

if __name__ == '__main__':
    server = sys.argv[-2]
    ssl_enabled = bool(sys.argv[-1])
    client = SMTPClient()
    client.connect(server, ssl_enabled)
    login = input("Login: ")
    password = input("Password: ")
    client.login(login, password)
    msg_from = input("From: ")
    msg_to = input("To: ")
    msg_header = input("Subject: ")
    client.set_header(msg_from, msg_to, msg_header)

    message = []
    s = input("> ")
    while s:
        message.append(s)
        s = input("> ")

    client.set_content(message)
    client.end_message()
    client.quit()
