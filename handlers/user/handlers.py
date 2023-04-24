from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.query.get import get_question
from database.query.get import get_establishments_by_city_name, get_same_answers, \
    get_establisments_cities, get_establishment_by_name, get_question_model, get_answer_by_id
from keyboards.keyboards import additional_contact_info_keyboard, welcome_keyboard, \
    user_main_keyboard, user_information_keyboard, go_menu_keyboard
from utils.states import SearchState


async def help_command(message: types.Message):
    await message.answer(get_question('user_help'), reply_markup=welcome_keyboard, parse_mode='Markdown')


async def get_info(message: types.Message):
    await message.answer('🔄 Загружаем информацию', reply_markup=go_menu_keyboard)
    await message.answer('📍 Выберите пункт, который вас интересует',
                         reply_markup=user_information_keyboard)


async def go_menu(message: types.Message):
    await message.answer('↩️ Возвращаемся в меню', reply_markup=user_main_keyboard, parse_mode='Markdown')


async def ask_a_question(message: types.Message, state: FSMContext):
    await message.answer("🔎 Введите свой вопрос ниже: ")
    await state.set_state(SearchState.search_value)


async def get_question_answer(message: types.Message, state: FSMContext):
    await message.answer(f'🔎 Ищем подходящий вариант {message.text.lower()}')

    questions = get_same_answers(message.text.lower())

    keyboard = types.InlineKeyboardMarkup()

    if len(questions) == 0:
        await message.answer('Извините, но я не смогу ответить на ваш вопрос\n'
                             'Вы можете воспользоваться технической поддержкой',
                             reply_markup=go_menu_keyboard)
    else:
        for answer in questions:
            question = get_question_model(answer)
            keyboard.add(types.InlineKeyboardButton(question.command_name,
                                                    callback_data=f'search_by '
                                                                  f'{question.id}'))
        await message.answer('🔎 Нашли для вас что-то похожее.\n'
                             'Выберите тот вариант, который вам '
                             'подходит:', reply_markup=keyboard)

    await state.finish()


async def search_by_id_callback(callback: types.CallbackQuery):
    text = f'📭**Ответ:** \n' \
           f'{get_answer_by_id(callback.data.replace("search_by ", ""))}'

    await callback.message.answer(text,
                                  reply_markup=go_menu_keyboard,
                                  parse_mode='Markdown')


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
    dp.register_message_handler(help_command, lambda message: message.text == '📍 Помощь')
    dp.register_message_handler(get_info, lambda message: message.text == 'ℹ️ Информация')
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(go_menu, commands=['menu'])
    dp.register_message_handler(go_menu, lambda message: message.text == '↩️ В меню')
    dp.register_message_handler(ask_a_question,
                                lambda message: message.text == '❔ Задать вопрос',
                                state=None)
    dp.register_message_handler(get_question_answer, state=SearchState.search_value)
    dp.register_callback_query_handler(find_establishments, text='info_establishment')
    dp.register_callback_query_handler(find_establishments_by_city_callback,
                                       Text(startswith='find_establisment_by_city '))
    dp.register_callback_query_handler(find_establishments_by_name_callback,
                                       Text(startswith='find_establisment_by_name '))
    dp.register_callback_query_handler(contact_info_callback,
                                       Text(startswith='info_contact'))
    dp.register_callback_query_handler(search_by_id_callback,
                                       Text(startswith='search_by '))
