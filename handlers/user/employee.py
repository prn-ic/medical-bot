from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from database.query.get import get_employees, get_employee_by_id, get_establishment_by_employee_id
from keyboards.keyboards import go_menu_keyboard


async def find_employees(callback: types.CallbackQuery):
    employees = get_employees()
    keyboard = types.InlineKeyboardMarkup()
    for employee in list(set(employees)):
        medic_name = f'{employee.user.surname} {employee.user.first_name} {employee.user.patronymic}'
        message_text = f'{medic_name}'
        keyboard.add(types.InlineKeyboardButton(message_text,
                                                callback_data=f'find_employee_by_id {employee.id}'))

    await callback.message.edit_text('🏥 Сотрудники:', reply_markup=keyboard)


async def find_employees_by_id_callback(callback: types.CallbackQuery):
    employee = get_employee_by_id(callback.data
                                  .replace('find_employee_by_id ', ''))

    medic_name = f'{employee.user.surname} {employee.user.first_name} {employee.user.patronymic}'
    establishment = get_establishment_by_employee_id(callback.data
                                                     .replace('find_employee_by_id ', ''))

    text = f'ℹ️ Информация ℹ️\n' \
           f'ФИО: <b>{medic_name}</b>\n' \
           f'Должность: <b>{employee.type.name}</b>\n' \
           f'Телефон: <b>{employee.user.phone}</b>\n' \
           f'E-mail: <b>{employee.user.email}</b>\n' \
           f'Город: <b>{establishment.city_name}</b>\n' \
           f'Филиал: <b>{establishment.name}</b>\n' \
           f'Адрес: <b>{establishment.address}</b>\n' \
           f'Доп. информация: <b>{employee.position}</b>\n'

    await callback.message.delete()

    await callback.message.answer(text, reply_markup=go_menu_keyboard,
                                  parse_mode="HTML")


def register_employee_handler(dp: Dispatcher):
    dp.register_callback_query_handler(find_employees, text='info_employees')
    dp.register_callback_query_handler(find_employees_by_id_callback,
                                       Text(startswith='find_employee_by_id '))
