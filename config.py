from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
import os
import logging

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv('BOT_TOKEN'))
dispatcher = Dispatcher(bot)
