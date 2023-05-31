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

logging.basicConfig(level=logging.INFO, format='[%(levelname)s]:[%(asctime)s] - %(name)s: %(message)s')
