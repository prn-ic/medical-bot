from aiogram import types, Dispatcher
from utils.database.questions import get_answer
from buttons.buttons import welcome_keyboard, user_main_keyboard, user_information_keyboard, go_menu_keyboard


async def start(message: types.Message):
    await message.answer(get_answer('start'), reply_markup=welcome_keyboard)


async def skip_auth(message: types.Message):
    await message.answer('Вы проигнорировали авторизацию.'
                         ' Без авторизации множество функций ограничено')
    await message.answer(get_answer('user_help'), reply_markup=user_main_keyboard, parse_mode="Markdown")


async def help_command(message: types.Message):
    await message.answer('Выбран')
    await message.answer(get_answer('user_help'), reply_markup=welcome_keyboard, parse_mode="Markdown")


async def get_info(message: types.Message):
    await message.answer('🔄 Загружаем информацию', reply_markup=go_menu_keyboard)
    await message.answer("📍 Выберите пункт, который вас интересует", reply_markup=user_information_keyboard)


async def go_menu(message: types.Message):
    await message.answer('↩️ Возвращаемся в меню', reply_markup=user_main_keyboard, parse_mode="Markdown")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(skip_auth, lambda message: message.text == '🚷 Продолжить без авторизации')
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(get_info, lambda message: message.text == 'ℹ️ Информация')
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(go_menu, commands=['menu'])
    dp.register_message_handler(go_menu, lambda message: message.text == '↩️ В меню')
