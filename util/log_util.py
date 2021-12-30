import logging
from logging.handlers import RotatingFileHandler

logger_name = "process_userproex"
logger4process_userproex = logging.getLogger(logger_name)
logger4process_userproex.setLevel(logging.DEBUG)

fh = RotatingFileHandler('../../logs/process_userproex.log', maxBytes=10*1024*1024,backupCount=5,encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# fmt = "%(asctime)-15s %(levelname)s %(filename)s [line:%(lineno)d] [%(process)d] %(message)s"
fmt = "%(asctime)-15s %(levelname)s %(filename)s [line:%(lineno)d] %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger4process_userproex.addHandler(fh)
logger4process_userproex.addHandler(ch)


logger_name = "prepare_comment_libsvm"
logger4prepare_comment_libsvm = logging.getLogger(logger_name)
logger4prepare_comment_libsvm.setLevel(logging.DEBUG)

fh = RotatingFileHandler('../../logs/prepare_comment_libsvm.log', maxBytes=10*1024*1024,backupCount=5,encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger4prepare_comment_libsvm.addHandler(fh)
logger4prepare_comment_libsvm.addHandler(ch)


logger_name = "prepare_movie_relation"
logger4prepare_movie_relation = logging.getLogger(logger_name)
logger4prepare_movie_relation.setLevel(logging.DEBUG)

fh = RotatingFileHandler('../../logs/prepare_movie_relation.log', maxBytes=10*1024*1024,backupCount=5,encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger4prepare_movie_relation.addHandler(fh)
logger4prepare_movie_relation.addHandler(ch)


logger_name = "movie_based_recall"
logger4movie_based_recall = logging.getLogger(logger_name)
logger4movie_based_recall.setLevel(logging.DEBUG)

fh = RotatingFileHandler('../../logs/movie_based_recall.log', maxBytes=10*1024*1024,backupCount=5,encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger4movie_based_recall.addHandler(fh)
logger4movie_based_recall.addHandler(ch)


logger_name = "prepare_comment_csv"
logger4prepare_comment_csv = logging.getLogger(logger_name)
logger4prepare_comment_csv.setLevel(logging.DEBUG)

fh = RotatingFileHandler('../../logs/prepare_comment_csv.log', maxBytes=10*1024*1024,backupCount=5,encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger4prepare_comment_csv.addHandler(fh)
logger4prepare_comment_csv.addHandler(ch)


logger_name = "model_based_fm_lr_rec"
logger4model_based_fm_lr_rec = logging.getLogger(logger_name)
logger4model_based_fm_lr_rec.setLevel(logging.DEBUG)

fh = RotatingFileHandler('../../logs/model_based_fm_lr_rec.log', maxBytes=10*1024*1024,backupCount=5,encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger4model_based_fm_lr_rec.addHandler(fh)
logger4model_based_fm_lr_rec.addHandler(ch)







