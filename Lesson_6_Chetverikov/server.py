import json
import socket
import sys
import logging
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, STATUS_CODE, STATUS
from common.utils import get_message, send_message
import logs.configs.server_log_config
from decors import log

SERVER_LOGGER = logging.getLogger('server')


@log
def message_status(message):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {message}')
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
        SERVER_LOGGER.critical(f'Попытка запуска сервера с недопустимым портом: {server_port}. '
                               f'Порт сервера должен быть в диапазоне от "1024" до "65535"')
        sys.exit(1)

    SERVER_LOGGER.info(f'Запущен сервер, адрес сервера: {server_ip} '
                       f'порт для подключений: {server_port} ')

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((server_ip, server_port))
    server_sock.listen(MAX_CONNECTIONS)

    while True:
        client_sock, client_addr = server_sock.accept()
        SERVER_LOGGER.info(f'Подключен клиент с адресом {client_addr}')
        try:
            message_from_client = get_message(client_sock)
            SERVER_LOGGER.info(f'Получено сообщение от клиента: {message_from_client}')
            response = message_status(message_from_client)
            SERVER_LOGGER.debug(f'Сформирован ответ клиенту: {response}')
            send_message(client_sock, response)
            SERVER_LOGGER.info(f'Закрытие соединения с клиентом: {client_addr}')
            client_sock.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалрсь декодировать JSON строку полученную '
                                f'от клиента: {client_addr}. Закрытие соединения.')
            client_sock.close()
        except ValueError:
            SERVER_LOGGER.error(f'От клиента: {client_addr} получены некоректные данные. '
                                f'Закрытие соединения.')
            client_sock.close()


if __name__ == "__main__":
    main()
