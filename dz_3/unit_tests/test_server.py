import sys
import unittest
sys.path.append('..')
from server import process_client_message
from common.constants import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestServer(unittest.TestCase):
    error_message = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_message = {RESPONSE: 200}

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_message)

    def test_no_action(self):
        """Ошибка если нет действия"""
        self.assertEqual(process_client_message(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.error_message)

    def test_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.assertEqual(process_client_message(
            {ACTION: 'prоbe', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.error_message)

    def test_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_message)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1.1'}), self.error_message)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Gu'}}), self.error_message)

# def server ничего не принимает и не отдает, поэтому тесты ей не нужны


if __name__ == '__main__':
    unittest.main()
