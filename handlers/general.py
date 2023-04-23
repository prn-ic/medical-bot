from aiogram import types, Dispatcher
from utils.database.questions import get_answer
from buttons.buttons import welcome_keyboard


async def start(message: types.Message):
    await message.answer(get_answer('start'), reply_markup=welcome_keyboard)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
