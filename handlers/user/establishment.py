from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from database.query.get import get_establishments_by_city_name, \
    get_establisment_cities, get_establishment_by_id
from keyboards.keyboards import go_menu_keyboard


async def find_establishments(callback: types.CallbackQuery):
    establishments = get_establisment_cities()
    keyboard = types.InlineKeyboardMarkup()
    for city in list(set(establishments)):
        keyboard.add(types.InlineKeyboardButton(city,
                                                callback_data=f'find_establisment_by_city {city}'))

    await callback.message.edit_text('🏥 Выберите свой город:', reply_markup=keyboard)


async def find_establishments_by_city_callback(callback: types.CallbackQuery):
    city = callback.data.replace('find_establisment_by_city ', '')
    establishments = get_establishments_by_city_name(city)
    keyboard = types.InlineKeyboardMarkup()
    for establishment in establishments:
        short_address = f'{establishment.name} на {establishment.address.split(",")[2]}'
        keyboard.add(types.InlineKeyboardButton(short_address,
                                                callback_data=f'find_establisment_by_id '
                                                              f'{establishment.id}'))

    await callback.message.edit_text(f'📍Филиалы в городе {city}📍\n'
                                     'Нажмите на город, чтобы '
                                     'получить подробную информацию', reply_markup=keyboard)


async def find_establishments_by_name_callback(callback: types.CallbackQuery):
    establishment = get_establishment_by_id(callback.data
                                            .replace('find_establisment_by_id ', ''))

    text = f'ℹ️ Информация об учреждении ℹ️\n' \
           f'Наименование учреждения:\n •<b>{establishment.name}</b>\n' \
           f'Адрес:\n •<b>{establishment.address}</b>\n' \
           f'График работы:\n •<b>{establishment.description}</b>\n' \
           f'Город:\n •<b>{establishment.city_name}</b>\n'

    await callback.message.delete()

    await callback.message.answer(text, reply_markup=go_menu_keyboard,
                                  parse_mode="HTML")
    await callback.message.answer('📍 Координаты на карте: 📍')
    await callback.bot.send_location(chat_id=callback.message.chat.id,
                                     latitude=establishment.coord_latitude,
                                     longitude=establishment.coord_longitude)


def register_establishment_handler(dp: Dispatcher):
    dp.register_callback_query_handler(find_establishments, text='info_establishment')
    dp.register_callback_query_handler(find_establishments_by_city_callback,
                                       Text(startswith='find_establisment_by_city '))
    dp.register_callback_query_handler(find_establishments_by_name_callback,
                                       Text(startswith='find_establisment_by_id '))
