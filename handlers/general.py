from aiogram import types, Dispatcher
from database.query.get import get_question
from keyboards.keyboards import welcome_keyboard, user_main_keyboard


async def start(message: types.Message):
    await message.answer(get_question('start'), reply_markup=welcome_keyboard)


async def skip_auth(message: types.Message):
    await message.answer(get_question('user_help'), reply_markup=user_main_keyboard, parse_mode="Markdown")


async def unhandled_command(message: types.Message):
    await message.answer("Извините, но такой команды не существует")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(skip_auth, lambda message: message.text == '🚷 Продолжить без авторизации')
    dp.register_message_handler(unhandled_command)
