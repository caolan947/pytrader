import logging
import logging.config
from datetime import datetime

logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True,})

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', '%Y-%m-%d_%I-%M-%S')

def config_logger(level=logging.INFO):
    handler = logging.FileHandler(filename=f"pytrader/logs/{datetime.now():%Y-%m-%d_%I-%M-%S}.log")        
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger