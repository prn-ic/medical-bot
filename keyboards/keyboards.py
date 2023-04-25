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

establishment_info_button = InlineKeyboardButton("🏥 Учреждения", callback_data="info_establishment")
employees_info_button = InlineKeyboardButton("👩‍🔬 Сотрудники", callback_data="info_employees")
contact_info_button = InlineKeyboardButton("📞 Контактная информация", callback_data="info_contact")

additional_contact_info_button = InlineKeyboardButton("Подробная информация",
                                                      url="http://orskgb.nitoich.tw1.ru"
                                                          "/%d0%be-%d0%b1%d0%be%d0%bb%d1%8c%d0%bd%d0%b8%d1%86%d0%b5/")

go_menu_button = InlineKeyboardButton("↩️ В меню", callback_data='go_menu')

# Keyboards
welcome_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(authenticate_button, skip_auth_button)
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
employee_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
user_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(ask_a_question_button,
                                                                                information_button,
                                                                                get_support_button,
                                                                                help_button,
                                                                                settings_button)
go_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(go_menu_button)
user_information_keyboard = InlineKeyboardMarkup(row_width=1).add(establishment_info_button,
                                                                  contact_info_button)
additional_contact_info_keyboard = InlineKeyboardMarkup(row_width=1).add(additional_contact_info_button)
not_found_answer_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(ask_a_question_button,
                                                                          get_support_button,
                                                                          go_menu_button)
