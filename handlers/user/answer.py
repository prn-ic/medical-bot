from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.query.get import get_question
from database.query.get import get_same_answers, get_answer_by_id
from keyboards.keyboards import not_found_answer_keyboard, go_menu_keyboard
from utils.states import SearchState


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


def register_answer_handler(dp: Dispatcher):
    dp.register_message_handler(ask_a_question,
                                lambda message: message.text == '❔ Задать вопрос',
                                state=None)
    dp.register_message_handler(get_question_answer,
                                lambda message: message.text == '❔ Задать вопрос',
                                state=SearchState.search_value)
    dp.register_message_handler(get_question_answer, state=SearchState.search_value)
    dp.register_callback_query_handler(search_by_id_callback,
                                       Text(startswith='search_by '))
