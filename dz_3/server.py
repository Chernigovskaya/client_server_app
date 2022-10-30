import argparse
import logging
import logs.server_log_config
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import sys
import json
from dz_3.common.constants import MAX_CONNECTIONS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR
from dz_3.common.utils import read_message, write_message
from decorat import log
from dz_3.errors import IncorrectDataRecivedError

#Инициализация логирования сервера.
LOGGER = logging.getLogger('server')


@log
def process_client_message(message):  # принимает словарь, парсит и дает ответ OK или не ОК
    LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # валидация
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@log
def create_arg_parser():
    """
    Парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():  # порт
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
        LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
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
            LOGGER.info(f'Установлено соедение с ПК {client_addr}')
            try:
                message_from_client = read_message(client)  # клиет шлет сообщение и функция возвращвет словарь
                LOGGER.debug(f'Получено сообщение {message_from_client}')
                print(message_from_client)
                response = process_client_message(message_from_client)  # распарсит ответ
                LOGGER.info(f'Cформирован ответ клиенту {response}')
                write_message(client, response)  # отправляет ответ клиенту
                LOGGER.debug(f'Соединение с клиентом {client_addr} закрывается.')
                client.close()
            except json.JSONDecodeError:
                LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                    f'клиента {client_addr}. Соединение закрывается.')
                client.close()
            except IncorrectDataRecivedError:
                LOGGER.error(f'От клиента {client_addr} приняты некорректные данные. '
                             f'Соединение закрывается.')
                client.close()
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
