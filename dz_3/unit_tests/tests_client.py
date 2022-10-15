import sys
import unittest
sys.path.append('..')
from common.constants import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR

from client import create_dict, process_answer


class TestClient(unittest.TestCase):

    def test_correct_answer(self):
        """Тест корректного запроса"""
        test = create_dict()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_answer(self):
        """Тест корректтного разбора ответа 200"""
        self.assertEqual(process_answer({RESPONSE: 200}), '200 : OK')

    def test_400_answer(self):
        """Тест корректного разбора 400"""
        self.assertEqual(process_answer({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, process_answer, {ERROR: 'Bad Request'})




if __name__ == '__main__':
    unittest.main()
