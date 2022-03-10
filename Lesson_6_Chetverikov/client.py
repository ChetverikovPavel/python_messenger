import socket
import sys
import time
import logging
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, TIME, \
    USER, ACCOUNT_NAME, PRESENCE, STATUS_CODE, STATUS
from common.utils import send_message, get_message
import logs.configs.client_log_config
from decors import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.info(f'Сформировано {PRESENCE} сообщение: {out}')
    return out


@log
def check_response(response):
    CLIENT_LOGGER.debug(f'Разбор ответа от сервера: {response}')
    if STATUS_CODE in response:
        return f'{response[STATUS_CODE]}: {response[STATUS]}'
    raise ValueError


def main():
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        CLIENT_LOGGER.error(f'Не указан сервер для подключения. '
                            f'Подключение со стандартными параметрами: '
                            f'Адрес сервера: {DEFAULT_IP_ADDRESS}, порт: {DEFAULT_PORT}')
        server_ip = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOGGER.critical(f'Попытка подключения к серверу с недопустимым портом: {server_port}. '
                               f'Порт сервера должен быть в диапазоне от "1024" до "65535"')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запуск клиента. Параметры сервера: адрес: {server_ip}, порт: {server_port}')
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((server_ip, server_port))
        message_to_server = create_presence()
        send_message(client_sock, message_to_server)

        response_from_server = get_message(client_sock)
        checked_response = check_response(response_from_server)
        client_sock.close()
        CLIENT_LOGGER.info(f'Ответ от сервера: {checked_response}')
    except ValueError:
        CLIENT_LOGGER.error(f'Получен некоректный ответ от сервера: {response_from_server}')
        client_sock.close()


if __name__ == '__main__':
    main()
