import argparse
import logging
import select
import time

import logs.server_log_config
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import sys
import json
from dz_3.common.constants import MAX_CONNECTIONS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER
from dz_3.common.utils import read_message, write_message
from decorat import log
from dz_3.errors import IncorrectDataRecivedError

# Инициализация логирования сервера.
LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list,
                           client):  # принимает словарь, парсит и отправляет словарь-ответ для клиента с результатом приёма.
    LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # валидация
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        write_message(client, {RESPONSE: 200})
        return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        write_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'})
        return


@log
def create_arg_parser():
    """
    Парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    if listen_port < 1023 or listen_port > 65536:
        LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                        f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    return listen_address, listen_port


def main():  # порт
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    Сначала обрабатываем порт:
     client.py 192.168.1.34 8080
    server.py -p 8080 -a 192.168.1.34
    """
    listen_address, listen_port = create_arg_parser()

    LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                f'адрес с которого принимаются подключения: {listen_address}. '
                f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет

    server_socket = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP (сетевой, потоковый)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # чтобы не ждать когда разблокируется после выключения
    server_socket.bind((listen_address, listen_port))  # Присваивает хост и порт
    server_socket.settimeout(0.5)

    # список клиентов , очередь сообщений
    clients = []
    messages = []
    # Слушаем порт
    server_socket.listen(MAX_CONNECTIONS)  # режим ожидания клиентов (слушает порт)
    # Основной цикл программы сервера

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_addr = server_socket.accept()  # запрос на соединение клиентом
        except OSError:
            pass
        else:
            LOGGER.info(f'Установлено соедение с ПК {client_addr}')
            clients.append(client)
        recv_data_lst = []
        send_data_lst = []
        err_lst = []
            # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass
                # принимаем сообщения и если там есть сообщения,
                # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(read_message(client_with_message), messages, client_with_message)
                except:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                        f'отключился от сервера.')
                    clients.remove(client_with_message)
            # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0], # тко отправил
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1] # текст сообщения
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    write_message(waiting_client, message)
                except:
                    LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
