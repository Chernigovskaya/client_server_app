import argparse
import logging
import select
import logs.server_log_config
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import sys
from common.constants import MAX_CONNECTIONS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, ERROR, MESSAGE, MESSAGE_TEXT, SENDER, RESPONSE_200, RESPONSE_400, DESTINATION, EXIT
from common.utils import read_message, write_message
from decorat import log


# Инициализация логирования сервера.
LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client, clients, names):  # принимает словарь, парсит и отправляет словарь-ответ для клиента с результатом приёма.
    """
        Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
        проверяет корректность, отправляет словарь-ответ в случае необходимости.
        :param message:
        :param messages_list:
        :param client:
        :param clients:
        :param names:
        :return:
        """
    LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # валидация
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        # Если такой пользователь ещё не зарегистрирован,
        # регистрируем, иначе отправляем ответ и завершаем соединение.
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            write_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            write_message(client, response)
            clients.remove(client)
            client.close()
        return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
        # Если клиент выходит
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    # Иначе отдаём Bad request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        write_message(client, response)
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


@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        write_message(names[message[DESTINATION]], message)
        LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


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
    # Словарь, содержащий имена пользователей и соответствующие им сокеты.
    names = dict()
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
                # принимаем сообщения и  если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(read_message(client_with_message), messages, client_with_message, clients, names)
                except Exception:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                        f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения, обрабатываем каждое.
        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
