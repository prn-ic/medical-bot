from aiogram import types, Dispatcher
from database.query.get import get_question
from keyboards.keyboards import user_main_keyboard


async def help_command(message: types.Message):
    await message.answer(get_question('user_help').answer, reply_markup=user_main_keyboard,
                         parse_mode='Markdown')


async def go_menu(message: types.Message):
    await message.answer('↩️ Возвращаемся в меню', reply_markup=user_main_keyboard, parse_mode='Markdown')


def register_common_handler(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(help_command, lambda message: message.text == '📍 Помощь')
    dp.register_message_handler(go_menu, commands=['menu'])
    dp.register_message_handler(go_menu, lambda message: message.text == '↩️ В меню')
