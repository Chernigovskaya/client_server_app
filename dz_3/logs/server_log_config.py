import sys
import os

import logging.handlers
sys.path.append('../')
from common.constants import ENCODING, LOGGING_LEVEL

#  Создать логгер - регистратор верхнего уроовня
log = logging.getLogger('server')
log.setLevel(LOGGING_LEVEL) # уровень

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')

# файловый обработчик
file_hand = logging.handlers.TimedRotatingFileHandler(path, when='D', interval=1, encoding=ENCODING)
file_hand.setLevel(logging.INFO)#  с уровнем INFO

# стримовый обработчик
# stream_hand = logging.StreamHandler() # передаем в поток
# stream_hand.setLevel(logging.INFO) #  с уровнем INFO

# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
# Создать объект Formatter
# Определить формат сообщений
server_formatter = logging.Formatter('%(asctime)s - %(levelname)-10s - %(module)-10s - %(message)s')

# подключить объект Formatter к обработчику
#stream_hand.setFormatter(server_formatter)
file_hand.setFormatter(server_formatter)


# Добавить обработчик к регистратору
#log.addHandler(stream_hand) # добавить в поток
log.addHandler(file_hand) # добавить в файл


if __name__ == '__main__':
    log.critical('Критическая ошибка')
    log.error('Ошибка')
    log.warning('Предупреждение')
    log.info('Информационное сообщение')
    log.debug('Отладочная информация')