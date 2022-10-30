import inspect
import sys
import traceback
import logging


def log(func_to_log):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        '''Обертка'''
        logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
        LOGGER = logging.getLogger(logger_name)

        result = func_to_log(*args, **kwargs)
        LOGGER.debug(
            f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}.'
            f'Вызов из модуля {func_to_log.__module__}.'
            f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return result
    return log_saver
