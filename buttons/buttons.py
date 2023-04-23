from aiogram.types import *

# Buttons
authenticate_button = KeyboardButton("🚻 Начать")
skip_auth_button = KeyboardButton("🚷 Продолжить без авторизации")
record_to_appointment_button = KeyboardButton("📋 Записаться к врачу")
ask_a_question_button = KeyboardButton("❔ Задать вопрос")
information_button = KeyboardButton("ℹ️ Информация")
get_support_button = KeyboardButton("☎️ Обратиться в поддержку")
help_button = KeyboardButton("📍 Помощь")
settings_button = KeyboardButton("🛠 Настройки")

# Keyboards
welcome_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(authenticate_button, skip_auth_button)
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
employee_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
user_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(record_to_appointment_button,
                                                                   ask_a_question_button,
                                                                   information_button,
                                                                   get_support_button,
                                                                   help_button,
                                                                   settings_button)


