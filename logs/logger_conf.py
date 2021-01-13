
import logging
from logging.handlers import RotatingFileHandler
from setting import LOG_DIR

def configure_logging(app):
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]
    # Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, ]
    handlers = []
    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)

    info_handler = RotatingFileHandler(LOG_DIR+'balance.log', maxBytes=10000, backupCount=1)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(verbose_formatter())
    handlers.append(info_handler)

    error_handler = RotatingFileHandler(LOG_DIR+'balance-error.log', maxBytes=10000, backupCount=3)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(verbose_formatter())
    handlers.append(error_handler)

    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.INFO)

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

