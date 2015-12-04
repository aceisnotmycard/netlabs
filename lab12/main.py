import sys
from lab12.pop3 import POP3Client
from lab12.smtp import SMTPClient

smtp_client = None
pop_client = None


def process_input():
    msg = str(input())
    if msg.startswith('/'):
        msg = msg[1:]
        command = msg.split(' ')
        if command[0] == 'list':
            pop_client.list()
        elif command[0] == 'help':
            print("""
/list – show messages in the inbox
/send – send message to somebody
/show <message position> – show specified message from list
/quit – close app
            """)
        elif command[0] == 'show':
            pop_client.show_message(int(command[1]))
        elif command[0] == 'send':
            msg_from = input("From: ")
            msg_to = input("To: ")
            msg_header = input("Subject: ")
            smtp_client.set_header(msg_from, msg_to, msg_header)

            message = []
            s = input("> ")
            while s:
                message.append(s)
                s = input("> ")
            smtp_client.set_content(message)
            smtp_client.end_message()
        elif command[0] == 'quit':
            pop_client.quit()
            smtp_client.quit()
            exit()


if __name__ == '__main__':
    pop_server = sys.argv[-3]
    smtp_server = sys.argv[-2]
    ssl_enabled = bool(sys.argv[-1])

    pop_client = POP3Client()
    pop_client.connect(pop_server, ssl_enabled)

    smtp_client = SMTPClient()
    smtp_client.connect(smtp_server, ssl_enabled)

    login = input("Login: ")
    password = input("Password: ")

    pop_client.login(login, password)
    smtp_client.login(login, password)
    while True:
        process_input()
