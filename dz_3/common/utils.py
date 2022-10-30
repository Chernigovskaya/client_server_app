import json
import sys
from dz_3.common.constants import MAX_PACKAGE_LENGTH, ENCODING
sys.path.append('../')
from decorat import log
from errors import IncorrectDataRecivedError, NonDictInputError


@log
# приняли сообщение и декодирование bytes => dict
def read_message(sock):  # (объект сокета)

    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)  # получили данные в байтах(2048)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(encoding=ENCODING)  # декодировали в строку-json
        if isinstance(json_response, str):
            response = json.loads(json_response)  # из строки-json в словарь
            if isinstance(response, dict):
                return response
            raise IncorrectDataRecivedError
        raise IncorrectDataRecivedError
    raise IncorrectDataRecivedError


@log
# закодировали и отправили
def write_message(sock, message):  # (объект сокета и сообщение в виде словаря)
    if not isinstance(message, dict):
        raise NonDictInputError
    json_message = json.dumps(message)  # словарь в json-строку
    encoded_message = json_message.encode(encoding=ENCODING)  # json-строку в байты
    sock.send(encoded_message)  # отправили байты
