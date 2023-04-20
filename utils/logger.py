from datetime import datetime
import logging
import os

FORMAT_PATTERN = '[%(levelname)s] %(asctime)s,%(msecs)d (%(name)s): %(message)s'
FILENAME_PATTERN = f"{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.txt"


def start_logging(logging_level: logging, log_path: str = 'log'):
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    logging.basicConfig(filename=f"{log_path}/{FILENAME_PATTERN}",
                        filemode="a+",
                        format=FORMAT_PATTERN,
                        datefmt='%H:%M:%S',
                        level=logging_level)
