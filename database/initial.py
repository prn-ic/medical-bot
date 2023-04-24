from database.models import *
import random
import uuid


random_uuid_generator = random.Random()

if __name__ == '__main__':
    db.create_tables([UserRole,
                      RecordType,
                      Establishment,
                      User,
                      EmployeeEstablishment,
                      UserInfo,
                      Question,
                      Record,
                      SupportTopic])

    # Start data
    user_role_source = [
        {'id': uuid.uuid4(), 'name': 'Admin'},
        {'id': uuid.uuid4(), 'name': 'Employee'},
        {'id': uuid.uuid4(), 'name': 'User'},
    ]
    UserRole.insert_many(user_role_source).execute()

    Question.insert(id=uuid.uuid4(),
                    command_name='start',
                    answer='Добро пожаловать в MedicalBot. С помощью нашего бота ты сможешь:\n'
                           '1)Ознакомиться с графиком работы интересующего вас учреждения\n'
                           '2) Узнать полезную для себя информацию\n'
                           '3) Записаться на прием врачу\n'
                           '4) Обратиться в техническую поддержку\n\n'
                           'Для продолжения рекомендуется авторизоваться').execute()

    Question.insert(id=uuid.uuid4(),
                    command_name='user_help',
                    answer='Вы можете использовать команды следующим образом:\n\n'
                           '📋 Записаться к врачу\n\n'
                           '├ __Данная кнопка позволяет записаться на прием к врачу,'
                           'которого вы желаете посетить (в случае, если запись '
                           'бесплатна)__\n'
                           '└ __Команда для ввода: **/record [ФИО]**__\n\n'
                           '❔ Задать вопрос\n\n'
                           '├ __Данная кнопка позволяет задать соответствующий вопрос,'
                           'интересующий вас, и ответит на него__\n'
                           '└ __Команда для ввода: **/ask [вопрос]**__\n\n'
                           'ℹ️ Информация\n\n'
                           '├ __Данная кнопка предоставляет подробную информацию,'
                           'касающуюся Орской больницы, филиалов, и так далее__\n'
                           '└ __Команда для ввода: **/info**__\n\n'
                           '☎️ Обратиться в поддержку\n\n'
                           '├ __Данная кнопка позволяет обратиться за помощью к '
                           'реальному человеку, в случае если вы не нашли ответ'
                           'на свой вопрос__\n'
                           '└ __Команда для ввода: **/support**__\n\n'
                           '📍 Помощь\n\n'
                           '├ __Данная кнопка выводит данное сообщение__\n'
                           '└ __Команда для ввода: **/help**\n\n__'
                           '🛠 Настройки\n\n'
                           '├ __Данная кнопка позволяет настроить бота__\n'
                           '└ __Команда для ввода: **/settings**\n\n__').execute()
