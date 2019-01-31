import logging
from logging.handlers import RotatingFileHandler

logger_name = "nossp_insp_logger"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

fh = RotatingFileHandler('nossp_insp.log', maxBytes=10*1024*1024,backupCount=5,encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# fmt = "%(asctime)-15s %(levelname)s %(filename)s [line:%(lineno)d] [%(process)d] %(message)s"
fmt = "%(asctime)-15s %(levelname)s %(filename)s [line:%(lineno)d] %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
