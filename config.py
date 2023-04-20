from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from utils import logger
import os
import logging

load_dotenv(find_dotenv())
bot = Bot(os.getenv('BOT_TOKEN'))
dispatcher = Dispatcher(bot)


if __debug__:
    logger.start_logging(logging_level=logging.DEBUG, log_path='log/debug')
else:
    logger.start_logging(logging_level=logging.INFO, log_path='log/release')
