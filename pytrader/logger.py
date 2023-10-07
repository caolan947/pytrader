import logging
import logging.config
from datetime import datetime

logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True,})

# TODO fix asctime format to be consistent with filename format
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def config_logger(level=logging.INFO):
    handler = logging.FileHandler(filename=f"pytrader/logs/{datetime.now():%d-%m-%Y_%I-%M-%S}.log")        
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# TODO remove debug code below
historical_logger = config_logger()
historical_records = [{'1':'2'},{'2':'3'},{'3':'4'}]
historical_logger.info('\n'.join(map(str, historical_records)))
