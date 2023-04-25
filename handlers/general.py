from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from utils.states import AuthState
from database.query.get import get_question, get_user_role_by_name
from database.commands.post import *
from keyboards.keyboards import welcome_keyboard, user_main_keyboard
import re


async def start(message: types.Message):
    await message.answer(get_question('start').answer, reply_markup=welcome_keyboard)


async def skip_auth(message: types.Message):
    await message.answer(get_question('user_help').answer,
                         reply_markup=user_main_keyboard,
                         parse_mode="Markdown")


async def auth(message: types.Message, state: FSMContext):
    await message.answer('Хорошо, приступим, для начала введи свою фамилию:')
    await state.set_state(AuthState.wait_firstname)


async def auth_set_firstname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer('🖊 Теперь введите свое имя: ')

    await state.set_state(AuthState.wait_patronymic)


async def auth_set_patronymic(message: types.Message, state: FSMContext):
    await state.update_data(firstname=message.text)
    await message.answer('🖊 Теперь введите свое отчество: ')

    await state.set_state(AuthState.wait_phone)


async def auth_set_phone(message: types.Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    await message.answer('🖊 Для того, чтобы с вами могли связаться, '
                         'укажите свой номер телефона:')

    await state.set_state(AuthState.wait_email)


async def auth_set_email(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer('🖊 Укажите свой адрес электронной почты:')

    await state.set_state(AuthState.wait_end)


async def auth_end_sign_in(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)

    user_data = await state.get_data()

    validate_phone_number_pattern = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?" \
                                    "[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"

    employee_role = get_user_role_by_name('Employee')
    employee_info = UserInfo()
    employee_user = User()
    employee_user.id = uuid.uuid4()
    employee_user.telegram_id = message.from_user.id
    create_user(employee_user)

    employee_info.role = employee_role
    employee_info.user = employee_user
    employee_info.first_name = user_data['firstname']
    employee_info.surname = user_data['surname']
    employee_info.patronymic = user_data['patronymic']
    employee_info.phone = user_data['phone']
    employee_info.email = user_data['email']

    try:
        if not (re.match(r"[^@]+@[^@]+\.[^@]+", user_data['email'])) or not \
                (re.match(validate_phone_number_pattern, user_data['phone'])):
            raise Exception('Invalid data')

        create_user_info(employee_info)

        await message.answer('✅Регистрация успешно завершена.✅\n'
                             'Ожидайте разрешения от администратора.\n'
                             'Вас уведомят в случае, если что-то '
                             'пойдет не так, либо регистрация '
                             'пройдет успешно')
    except:
        await message.answer("❌ Регистрация не удалась! ❌\n"
                             "Возможные причины: \n• Уже существует сотрудник с данным номером телефона\n"
                             "• Уже существует сотрудник с данным адресом электронной почты\n"
                             "• Неправильно указаны данные")

    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(skip_auth, lambda message: message.text == '🚷 Продолжить без авторизации')
    dp.register_message_handler(auth, lambda message: message.text == '🚻 Начать', state=None)
    dp.register_message_handler(auth_set_firstname, state=AuthState.wait_firstname)
    dp.register_message_handler(auth_set_patronymic, state=AuthState.wait_patronymic)
    dp.register_message_handler(auth_set_phone, state=AuthState.wait_phone)
    dp.register_message_handler(auth_set_email, state=AuthState.wait_email)
    dp.register_message_handler(auth_end_sign_in, state=AuthState.wait_end)
