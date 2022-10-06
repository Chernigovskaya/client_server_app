import sys
import json
from socket import AF_INET, SOCK_STREAM, socket
import time

from common.utils import read_message, write_message
from dz_3.common.constants import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR


def create_dict(account_name='Guest'):  # Функция генерирует запрос о присутствии клиента. делает словарь

    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_answer(message):  # парсит ответ

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def client():
    '''Загружаем параметы коммандной строки
    client.py 192.168.1.34 8080
    server.py -p 8080 -a 192.168.1.34
    '''
    try:
        server_addr = sys.argv[1]  # парсит хост
        server_port = int(sys.argv[2])  # парсит порт
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_addr = DEFAULT_IP_ADDRESS  # иначе из константы
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    client_socket = socket(AF_INET, SOCK_STREAM)  # создает сокет
    client_socket.connect((server_addr, server_port))  # подключается
    message_to_server = create_dict()
    write_message(client_socket, message_to_server)  # отправляет сообщение
    try:
        answer = process_answer(read_message(client_socket))  # получает ответ и парсит
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    client()
