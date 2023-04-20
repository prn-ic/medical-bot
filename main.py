from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv
import logging
import os


load_dotenv(find_dotenv())
bot = Bot(os.getenv('BOT_TOKEN'))
dispatcher = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
