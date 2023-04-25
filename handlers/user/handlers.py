import uuid

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from database.models import SupportTopic, SupportTopicMessage
from database.query.get import get_question
from database.commands.post import create_support_topic, create_support_topic_message
from database.query.get import get_establishments_by_city_name, get_same_answers, \
    get_establisments_cities, get_establishment_by_id, get_answer_by_id
from keyboards.keyboards import additional_contact_info_keyboard, not_found_answer_keyboard, \
    user_main_keyboard, user_information_keyboard, go_menu_keyboard
from utils.states import SearchState, SupportState


async def help_command(message: types.Message):
    await message.answer(get_question('user_help').answer, reply_markup=user_main_keyboard,
                         parse_mode='Markdown')


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
    await message.answer(f'🔎 Ищем подходящий вариант ...')

    questions = get_same_answers(message.text.lower())

    keyboard = types.InlineKeyboardMarkup()

    if len(questions) == 0:
        await message.answer('Извините, но я не смогу ответить на ваш вопрос\n'
                             'Вы можете воспользоваться технической поддержкой,'
                             ' или задать вопрос заново',
                             reply_markup=not_found_answer_keyboard)
    else:
        for answer in questions:
            question = get_question(answer)
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
    for city in list(set(establishments)):
        keyboard.add(types.InlineKeyboardButton(city,
                                                callback_data=f'find_establisment_by_city {city}'))

    await callback.message.edit_text('🏥 Выберите свой город:', reply_markup=keyboard)


async def find_establishments_by_city_callback(callback: types.CallbackQuery):
    city = callback.data.replace('find_establisment_by_city ', '')
    establishments = get_establishments_by_city_name(city)
    keyboard = types.InlineKeyboardMarkup()
    for establishment in establishments:
        keyboard.add(types.InlineKeyboardButton(establishment.name,
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

    await callback.message.answer(text, reply_markup=go_menu_keyboard,
                                  parse_mode="HTML")
    await callback.message.answer('📍 Координаты на карте: 📍')
    await callback.bot.send_location(chat_id=callback.message.chat.id,
                                     latitude=establishment.coord_latitude,
                                     longitude=establishment.coord_longitude)


async def contact_info_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(get_question('contact_info').answer,
                                     reply_markup=additional_contact_info_keyboard,
                                     parse_mode='HTML')


async def get_support(message: types.Message, state: FSMContext):
    await message.answer('✉️ Для того, чтобы задать вопрос, введите его ниже. ✉️\n\n'
                         'Поддержка свяжется с вами, и вы получите уведомление '
                         'с ответом.')
    await state.set_state(SupportState.wait_content)


async def send_answer_to_support(message: types.Message, state: FSMContext):
    try:
        support_topic = SupportTopic()
        topic_message = SupportTopicMessage()
        support_topic.id = uuid.uuid4()
        support_topic.responder_telegram_id = message.from_user.id

        topic_message.topic = support_topic
        topic_message.content = message.text

        create_support_topic(support_topic)
        create_support_topic_message(topic_message)

        await message.answer('✅Ваш ответ отправлен в поддержку.✅\n'
                             'Содержание ответа: \n'
                             f'```{message.text}```'
                             'Ожидайте ответа!', reply_markup=user_main_keyboard, parse_mode='Markdown')

    except:
        await message.answer('❌Ваш ответ не был отправлен в поддержку.❌\n'
                             'Попробуйте позже!', reply_markup=user_main_keyboard)

    finally:
        await state.finish()


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
                                       Text(startswith='find_establisment_by_id '))
    dp.register_callback_query_handler(contact_info_callback,
                                       Text(startswith='info_contact'))
    dp.register_callback_query_handler(search_by_id_callback,
                                       Text(startswith='search_by '))
    dp.register_message_handler(get_support,
                                lambda message: message.text == '☎️ Обратиться в поддержку',
                                state=None)
    dp.register_message_handler(send_answer_to_support, state=SupportState.wait_content)
