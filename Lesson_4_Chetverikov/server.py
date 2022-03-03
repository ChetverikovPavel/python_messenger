import json
import socket
import sys
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, STATUS_CODE, STATUS
from common.utils import get_message, send_message


def message_status(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {
            STATUS_CODE: 200,
            STATUS: 'OK'
        }
    else:
        return {
            STATUS_CODE: 400,
            STATUS: 'Bad Request'
        }


def main():
    if '-a' in sys.argv:
        server_ip = sys.argv[sys.argv.index('-a') + 1]
    else:
        server_ip = DEFAULT_IP_ADDRESS

    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = DEFAULT_PORT
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        print('Порт сервера должен быть в диапазоне от "1024" до "65535"')
        sys.exit(1)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((server_ip, server_port))
    server_sock.listen(MAX_CONNECTIONS)

    while True:
        client_sock, client_addr = server_sock.accept()

        try:
            message_from_client = get_message(client_sock)
            print(message_from_client)
            response = message_status(message_from_client)
            send_message(client_sock, response)
            client_sock.close()
        except(ValueError, json.JSONDecodeError):
            print('error')
            client_sock.close()


if __name__ == "__main__":
    main()
