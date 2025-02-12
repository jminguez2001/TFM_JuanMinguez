import sys
import logging
import logging.config
from concurrent_log_handler import ConcurrentRotatingFileHandler
from logging import StreamHandler
from logging.handlers import SMTPHandler

import globalParameters


def initLogger(processName, origin):
    """
    initLogger inicializa y configura un logger para un proceso específico.

    Args:
        processName (str): nombre del proceso para el logger.
        origin (str): origen del log (usado en el nombre del archivo de log).

    Returns:
        logging.Logger: objeto logger configurado.
    """

    logger = logging.getLogger(processName)
    logger.setLevel(logging.DEBUG)
    rotatingFilehandler = ConcurrentRotatingFileHandler(globalParameters.path + "/logs/"+origin+".log", maxBytes=20000, backupCount=10)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rotatingFilehandler.setFormatter(formatter)
    logger.addHandler(rotatingFilehandler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    handler = ConcurrentRotatingFileHandler(globalParameters.path + "/logs/"+origin+"_error.log", maxBytes=20000, backupCount=10)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)

    return logger