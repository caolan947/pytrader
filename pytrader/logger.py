import logging
import logging.config
from datetime import datetime

logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True})

formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', '%Y-%m-%d_%H-%M-%S')

def config_logger(level=logging.INFO):
    file_name = f"logs/{datetime.now():%Y-%m-%d_%H-%M-%S}.log"

    handler = logging.FileHandler(filename=file_name)        
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
