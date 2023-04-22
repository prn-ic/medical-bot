from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from utils.logger import txt_logger
from database.models import migrate
import os
import logging

load_dotenv(find_dotenv())
bot = Bot(os.getenv('BOT_TOKEN'))
dispatcher = Dispatcher(bot)


if __debug__:
    txt_logger.start_logging(logging_level=logging.DEBUG, log_path='log/debug')
    migrate()
else:
    txt_logger.start_logging(logging_level=logging.INFO, log_path='log/release')
