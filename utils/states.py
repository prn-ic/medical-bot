from aiogram.dispatcher.filters.state import StatesGroup, State


class SearchState(StatesGroup):
    search_value = State()


class AuthState(StatesGroup):
    wait_firstname = State()
    wait_surname = State()
    wait_patronymic = State()
    wait_phone = State()
    wait_email = State()
    wait_accept_notify = State()


class EmployeeAuthState(StatesGroup):
    wait_position = State()
