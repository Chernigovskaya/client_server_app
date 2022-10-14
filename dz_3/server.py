from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import sys
import json
from dz_3.common.constants import MAX_CONNECTIONS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR
from dz_3.common.utils import read_message, write_message


def process_client_message(message):  # принимает словарь, парсит и дает ответ OK или не ОК

    # валидация
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def server():  # порт
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    Сначала обрабатываем порт:
     client.py 192.168.1.34 8080
    server.py -p 8080 -a 192.168.1.34
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])  # если есть то достает
        else:
            listen_port = DEFAULT_PORT  # если нет то из constants
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)  # выход при ошибке
    except ValueError:
        print('Номер порта может быть указано только в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружает какой адрес слушать (хост)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    server_socket = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP (сетевой, потоковый)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # чтобы не ждать когда разблокируется после выключения
    server_socket.bind((listen_address, listen_port))  # Присваивает хост и порт

    server_socket.listen(MAX_CONNECTIONS)  # режим ожидания клиентов (слушает порт)

    try:
        while True:
            client, client_addr = server_socket.accept()  # запрос на соединение клиентом
            try:
                message_from_client = read_message(client)  # клиет шлет сообщение и функция возвращвет словарь
                print(message_from_client)
                response = process_client_message(message_from_client)  # распарсит ответ
                write_message(client, response)  # отправляет ответ клиенту
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('Принято некорректное сообщение от клиента.')
                client.close()
    finally:
        server_socket.close()


if __name__ == '__main__':
    server()
