import socket
import sys
import time
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, TIME, \
    USER, ACCOUNT_NAME, PRESENCE, STATUS_CODE, STATUS
from common.utils import send_message, get_message


def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def check_response(response):
    if STATUS_CODE in response:
        return f'{response[STATUS_CODE]}: {response[STATUS]}'


def main():
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_ip = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Порт сервера должен быть в диапазоне от "1024" до "65535"')
        sys.exit(1)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((server_ip, server_port))
    message_to_server = create_presence()
    send_message(client_sock, message_to_server)

    response_from_server = check_response(get_message(client_sock))
    client_sock.close()

    print(response_from_server)


if __name__ == '__main__':
    main()
