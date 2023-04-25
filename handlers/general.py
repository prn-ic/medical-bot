from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from utils.states import AuthState
from database.query.get import get_question
from keyboards.keyboards import welcome_keyboard, user_main_keyboard


async def start(message: types.Message):
    await message.answer(get_question('start').answer, reply_markup=welcome_keyboard)


async def skip_auth(message: types.Message):
    await message.answer(get_question('user_help').answer,
                         reply_markup=user_main_keyboard,
                         parse_mode="Markdown")


async def auth(message: types.Message, state: FSMContext):
    await message.answer('Хорошо, приступим, для начала введи свою фамилию:')
    await state.set_state(AuthState.wait_surname)


async def auth_set_firstname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer('🖊 Теперь введите свое имя: ')

    await state.set_state(AuthState.wait_firstname)


async def auth_set_patronymic(message: types.Message, state: FSMContext):
    await state.update_data(firstname=message.text)
    await message.answer('🖊 Теперь введите свое отчество: ')


async def auth_set_phone(message: types.Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    await message.answer('🖊 Для того, чтобы с вами могли связаться, '
                         'укажите свой номер телефона:')

    await state.set_state(AuthState.wait_phone)


async def auth_set_email(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer('🖊 Укажите свой адрес электронной почты:')

    await state.set_state(AuthState.wait_phone)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(skip_auth, lambda message: message.text == '🚷 Продолжить без авторизации')
