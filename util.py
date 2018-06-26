import os
import logging
from functools import wraps


def get_path(*path):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, *path)


def log(level=None, name=None):
    try:
        os.makedirs(get_path('logs'))
    except FileExistsError:
        pass

    def deco(func):
        """
        logging handler: file, stream
        decorator

        :return:
        """
        log_name = name if name else '.'.join([func.__module__, func.__name__])
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        log_formatter = logging.Formatter(
                '[%(levelname)s] %(asctime)s %(message)s')

        file_handler = logging.FileHandler(
                get_path('logs', 'main.log'), encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(log_formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal level
            if level is None:
                level = logging.DEBUG

            if level == logging.INFO:
                msg = log_name
            else:
                msg = log_name + repr(args) + repr(kwargs)

            logger.log(level, msg)
            return func(*args, **kwargs)

        return wrapper

    return deco
