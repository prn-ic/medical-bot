from aiogram import types, Dispatcher
from database.query.get import get_question, get_symptoms
from keyboards.keyboards import user_main_keyboard


async def help_command(message: types.Message):
    await message.answer(get_question('user_help').answer, reply_markup=user_main_keyboard,
                         parse_mode='Markdown')


async def go_symptoms(message: types.Message):
    symptoms = get_symptoms()
    keyboard = types.InlineKeyboardMarkup()
    for symptom in symptoms:
        keyboard.add(types.InlineKeyboardButton(symptom.name,
                                                callback_data=f'select_symptom '
                                                              f'{symptom.id}|1'))

    await message.answer('Что вас беспокоит?', reply_markup=keyboard)


async def go_menu(message: types.Message):
    await message.answer('↩️ Возвращаемся в меню', reply_markup=user_main_keyboard, parse_mode='Markdown')


def register_common_handler(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(help_command, lambda message: message.text == '📍 Помощь')
    dp.register_message_handler(go_menu, commands=['menu'])
    dp.register_message_handler(go_menu, lambda message: message.text == '↩️ В меню')
    dp.register_message_handler(go_symptoms, lambda message: message.text == '❤️ Симптомы')
