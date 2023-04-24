from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from database.query.get import get_question
from database.query.get import get_establishments_by_city_name, get_establisments_cities, get_establishment_by_name
from keyboards.keyboards import additional_contact_info_keyboard, welcome_keyboard, \
    user_main_keyboard, user_information_keyboard, go_menu_keyboard


async def help_command(message: types.Message):
    await message.answer('Выбран')
    await message.answer(get_question('user_help'), reply_markup=welcome_keyboard, parse_mode='Markdown')


async def get_info(message: types.Message):
    await message.answer('🔄 Загружаем информацию', reply_markup=go_menu_keyboard)
    await message.answer('📍 Выберите пункт, который вас интересует', reply_markup=user_information_keyboard)


async def go_menu(message: types.Message):
    await message.answer('↩️ Возвращаемся в меню', reply_markup=user_main_keyboard, parse_mode='Markdown')


async def get_a_question(message: types.Message):
    await message.answer('✉️ Для того, чтобы задать вопрос, используйте команду:\n'
                         '``` /ask [вопрос]```\n'
                         'Пример:\n'
                         '``` /ask Кто работает завтра?```', reply_markup=go_menu_keyboard,
                         parse_mode="Markdown")


async def find_establishments(callback: types.CallbackQuery):
    establishments = get_establisments_cities()
    keyboard = types.InlineKeyboardMarkup()
    for city in establishments:
        keyboard.add(types.InlineKeyboardButton(city,
                                                callback_data=f'find_establisment_by_city {city}'))

    await callback.message.edit_text('🏥 Выберите свой город:', reply_markup=keyboard)


async def find_establishments_by_city_callback(callback: types.CallbackQuery):
    establishments = get_establishments_by_city_name(callback.data
                                                     .replace('find_establisment_by_city ', ''))
    keyboard = types.InlineKeyboardMarkup()
    for establishment in establishments:
        keyboard.add(types.InlineKeyboardButton(establishment.name,
                                                callback_data=f'find_establisment_by_name '
                                                              f'{establishment.name}'))

    await callback.message.edit_text('📍Вот что удалось найти📍\n'
                                     'Нажмите на город, чтобы '
                                     'получить подробную информацию', reply_markup=keyboard)


async def find_establishments_by_name_callback(callback: types.CallbackQuery):
    establishment = get_establishment_by_name(callback.data
                                              .replace('find_establisment_by_name ', ''))

    text = f'ℹ️ Информация об учреждении ℹ️\n' \
           f'Наименование учреждения: <b>{establishment.name}</b>\n' \
           f'Город: <b>{establishment.city_name}</b>\n'

    await callback.message.answer(text, reply_markup=go_menu_keyboard,
                                  parse_mode="HTML")
    await callback.message.answer('📍 Координаты на карте: 📍')
    await callback.bot.send_location(chat_id=callback.message.chat.id,
                                     latitude=establishment.coord_latitude,
                                     longitude=establishment.coord_longitude)


async def contact_info_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(get_question('contact_info'),
                                     reply_markup=additional_contact_info_keyboard,
                                     parse_mode='HTML')


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(get_info, lambda message: message.text == 'ℹ️ Информация')
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(go_menu, commands=['menu'])
    dp.register_message_handler(go_menu, lambda message: message.text == '↩️ В меню')
    dp.register_message_handler(get_a_question, lambda message: message.text == '❔ Задать вопрос')
    dp.register_callback_query_handler(find_establishments, text='info_establishment')
    dp.register_callback_query_handler(find_establishments_by_city_callback,
                                       Text(startswith='find_establisment_by_city '))
    dp.register_callback_query_handler(find_establishments_by_name_callback,
                                       Text(startswith='find_establisment_by_name '))
    dp.register_callback_query_handler(contact_info_callback,
                                       Text(startswith='info_contact'))
