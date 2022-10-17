import argparse
import logging
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import sys
import json
from dz_3.common.constants import MAX_CONNECTIONS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR
from dz_3.common.utils import read_message, write_message


#Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


def process_client_message(message):  # принимает словарь, парсит и дает ответ OK или не ОК
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # валидация
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def create_arg_parser():
    """
    Парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def server():  # порт
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    Сначала обрабатываем порт:
     client.py 192.168.1.34 8080
    server.py -p 8080 -a 192.168.1.34
    """

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    if listen_port < 1023 or listen_port > 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')


    # Готовим сокет

    server_socket = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP (сетевой, потоковый)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # чтобы не ждать когда разблокируется после выключения
    server_socket.bind((listen_address, listen_port))  # Присваивает хост и порт
    # Слушаем порт
    server_socket.listen(MAX_CONNECTIONS)  # режим ожидания клиентов (слушает порт)

    try:
        while True:
            client, client_addr = server_socket.accept()  # запрос на соединение клиентом
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_addr}')
            try:
                message_from_client = read_message(client)  # клиет шлет сообщение и функция возвращвет словарь
                SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
                response = process_client_message(message_from_client)  # распарсит ответ
                SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
                write_message(client, response)  # отправляет ответ клиенту
                SERVER_LOGGER.debug(f'Соединение с клиентом {client_addr} закрывается.')
                client.close()
            except json.JSONDecodeError:
                SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                    f'клиента {client_addr}. Соединение закрывается.')
                client.close()
    finally:
        server_socket.close()


if __name__ == '__main__':
    server()
