from aiogram.dispatcher.filters.state import StatesGroup, State


class SearchState(StatesGroup):
    search_value = State()
