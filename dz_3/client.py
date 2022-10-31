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
    RESPONSE, ERROR, MESSAGE, SENDER, MESSAGE_TEXT
from errors import ReqFieldMissingError, ServerError
from decorat import log
# Инициализация клиентского логера
LOGGER = logging.getLogger('client')


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


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
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
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


@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if server_port < 1023 or server_port > 65536:
        LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f'В качестве порта может быть указано только число в диапазоне от 1024 до 65535. Клиент завершается.')
        sys.exit(1)
    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    '''Загружаем параметы коммандной строки
    client.py 192.168.1.34 8080
    server.py -p 8080 -a 192.168.1.34 '''

    server_address, server_port, client_mode = arg_parser()

    LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, порт: {server_port},'
                f'порт: {server_port}, режим работы: {client_mode}')

    # Инициализация сокета и обмен
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)  # создает сокет
        client_socket.connect((server_address, server_port))  # подключается
        write_message(client_socket, create_dict())  # отправляет сообщение
        answer = process_answer(read_message(client_socket))  # получает ответ и парсит
        LOGGER.info(f'Принят ответ от сервера {answer}')
        print(f'Установленно соединение с сервером.')
    except json.JSONDecodeError:
        LOGGER.error('Не удалось декодировать сообщение сервера.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, конечный компьютер отверг запрос на подключение.')
        sys.exit(1)

    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    write_message(client_socket, create_message(client_socket))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(read_message(client_socket))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
