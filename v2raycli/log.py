import logging
from typing import Union

LOGGING_LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]


def parse_log_level(level: Union[str, int]) -> int:
    if isinstance(level, int):
        if level not in {logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR}:
            raise ValueError(f'Unknown logging level value - {level!r}.')
        return level

    elif isinstance(level, str):
        level = level.upper().strip()
        if level in {'DEBUG'}:
            return logging.DEBUG
        elif level in {'INFO', 'INFORMATION'}:
            return logging.INFO
        elif level in {'WARNING', 'WARN'}:
            return logging.WARNING
        elif level in {'ERROR', 'ERR', 'FATAL'}:
            return logging.ERROR
        else:
            raise ValueError(f'Unknown logging level name - {level!r}.')

    else:
        raise TypeError(f'Unknown logging level type - {level!r}.')


def get_generic_stdout_logging(level: Union[str, int] = logging.INFO):
    return {
        "loglevel": logging.getLevelName(parse_log_level(level)).lower(),
        "access": "",
        "error": ""
    }
