from aiogram import types, Dispatcher
from database.query.get import get_question
from keyboards.keyboards import welcome_keyboard, user_main_keyboard


async def start(message: types.Message):
    await message.answer(get_question('start').answer, reply_markup=welcome_keyboard)


async def skip_auth(message: types.Message):
    await message.answer(get_question('user_help').answer, reply_markup=user_main_keyboard, parse_mode="Markdown")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(skip_auth, lambda message: message.text == '🚷 Продолжить без авторизации')
