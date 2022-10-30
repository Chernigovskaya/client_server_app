import argparse
import logging
import logs.client_log_config
import sys
import json
from socket import AF_INET, SOCK_STREAM, socket
import time
from errors import ReqFieldMissingError
from common.utils import read_message, write_message
from common.constants import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR
from decorat import log
# Инициализация клиентского логера
LOGGER = logging.getLogger('client')


@log
def create_dict(account_name='Guest'):  # Функция генерирует запрос о присутствии клиента. делает словарь

    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_answer(message):  # парсит ответ
    LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


@log
def create_arg_parser():
    """
    Создаём парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    '''Загружаем параметы коммандной строки
    client.py 192.168.1.34 8080
    server.py -p 8080 -a 192.168.1.34
    '''
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    if server_port < 1023 or server_port > 65536:
        LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f'В качестве порта может быть указано только число в диапазоне от 1024 до 65535. Клиент завершается.')
        sys.exit(1)
    LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, порт: {server_port}')


    # Инициализация сокета и обмен
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)  # создает сокет
        client_socket.connect((server_address, server_port))  # подключается
        message_to_server = create_dict()
        write_message(client_socket, message_to_server)  # отправляет сообщение
        answer = process_answer(read_message(client_socket))  # получает ответ и парсит
        LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        LOGGER.error('Не удалось декодировать сообщение сервера.')
    except ReqFieldMissingError as missing_error:
        LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
    except ConnectionRefusedError:
        LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
