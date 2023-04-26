from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from database.query.get import get_question
from keyboards.keyboards import additional_contact_info_keyboard,\
    user_information_keyboard, go_menu_keyboard


async def get_info(message: types.Message):
    await message.answer('🔄 Загружаем информацию', reply_markup=go_menu_keyboard)
    await message.answer('📍 Выберите пункт, который вас интересует',
                         reply_markup=user_information_keyboard)


async def contact_info_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(get_question('contact_info').answer,
                                     reply_markup=additional_contact_info_keyboard,
                                     parse_mode='HTML')


def register_information_handler(dp: Dispatcher):
    dp.register_message_handler(get_info, lambda message: message.text == 'ℹ️ Информация')
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_callback_query_handler(contact_info_callback,
                                       Text(startswith='info_contact'))
