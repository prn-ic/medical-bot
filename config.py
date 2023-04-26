from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from utils.logger import txt_logger
from handlers.general import register_user_handlers
import os
import logging

load_dotenv(find_dotenv())
bot = Bot(os.getenv('BOT_TOKEN'))
dispatcher = Dispatcher(bot, storage=MemoryStorage())

register_user_handlers(dispatcher)

if __debug__:
    txt_logger.start_logging(logging_level=logging.DEBUG, log_path='log/debug')
else:
    txt_logger.start_logging(logging_level=logging.INFO, log_path='log/release')
