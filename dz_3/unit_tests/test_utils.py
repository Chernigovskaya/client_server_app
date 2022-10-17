import sys
import unittest
import json
sys.path.append('..')
print(sys.path)
from common.constants import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.utils import read_message, write_message


class TestSocket:
    """Тестовый класс для тестирования отправки и получения,
    при создании требует словарь, который будет прогоняться
    через тестовую функцию
    """
    def __init__(self, test_message): #создает словарь
        self.test_message = test_message
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """Тестовая функция отправки, корректно кодирует сообщение,
        так-же сохраняет то, что должно быть отправлено в сокет.
        message_to_send - то, что отправляем в сокет
        """
        json_test_message = json.dumps(self.test_message) # из словаря строку получает
        self.encoded_message = json_test_message.encode(ENCODING) # кодирует сообщение
        self.received_message = message_to_send # сохраняем что должно было отправлено в сокет

    def recv(self, max_len):
        """Получаем данные из сокета"""
        json_test_message = json.dumps(self.test_message)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    """Тестовый класс, собственно выполняющий тестирование"""

    test_message_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_message_recv_ok = {RESPONSE: 200}
    test_message_recv_error = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_message_ok(self):
        """Тестируем корректность работы функции отправки,
        создадим тестовый сокет и проверим корректность отправки словаря
        """
        test_socket = TestSocket(self.test_message_send) # экземпляр тестового словаря, хранит собственно тестовый словарь
        write_message(test_socket, self.test_message_send)# вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        # Проверка корректности кодирования словаря.
        self.assertEqual(test_socket.encoded_message, test_socket.received_message) # Сравниваем результат кодирования и результат от тестируемой функции
        self.assertRaises(TypeError, write_message, test_socket, [1, 2]) # дополнительно, проверим генерацию исключения, при не словаре на входе,
                                                                            # и здесь использован следующий формат assertRaises:
                                                                            # <<self.assertRaises(TypeError, test_function, args)>>

    def test_get_message(self):
        """Тест функции приёма сообщения"""

        test_sock_ok = TestSocket(self.test_message_recv_ok)
        test_sock_err = TestSocket(self.test_message_recv_error)
        self.assertEqual(read_message(test_sock_ok), self.test_message_recv_ok)   # тест корректной расшифровки корректного словаря
        self.assertEqual(read_message(test_sock_err), self.test_message_recv_error) # тест корректной расшифровки ошибочного словаря


if __name__ == '__main__':
    unittest.main()
