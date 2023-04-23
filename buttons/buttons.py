from aiogram.types import *

# Buttons
authenticate_button = KeyboardButton("Начать")
skip_auth_button = KeyboardButton("Продолжить без авторизации")

# Keyboards
welcome_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(authenticate_button, skip_auth_button)
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
employee_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


