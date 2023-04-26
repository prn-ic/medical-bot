from aiogram.dispatcher.filters.state import StatesGroup, State


class SearchState(StatesGroup):
    search_value = State()


class SupportState(StatesGroup):
    wait_content = State()


class AuthState(StatesGroup):
    wait_firstname = State()
    wait_surname = State()
    wait_patronymic = State()
    wait_phone = State()
    wait_email = State()
    wait_accept_notify = State()
    wait_role = State()
    wait_end = State()


class SymptomState(StatesGroup):
    wait_causes_list = State()
    wait_causes_solution_list = State()
    wait_cause_score = State()
    wait_current_cause = State()
    wait_solution = State()


class EmployeeAuthState(StatesGroup):
    wait_position = State()
