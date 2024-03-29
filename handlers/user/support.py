from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from database.models import SupportTopic, SupportTopicMessage
from database.commands.post import create_support_topic, create_support_topic_message
from keyboards.keyboards import user_main_keyboard
from utils.states import SupportState
import uuid


async def get_support(message: types.Message, state: FSMContext):
    await message.answer('✉️ Для того, чтобы задать вопрос, укажите свою почту. ✉️\n\n'
                         'Поддержка свяжется с вами, и вы получите уведомление '
                         'с ответом.')
    await state.set_state(SupportState.wait_contact)


async def send_contacts(message: types.Message, state: FSMContext):
    await message.answer('✉️ Теперь введите свой вопрос ниже. ✉️')
    await state.update_data(contact=message.text)
    await state.set_state(SupportState.wait_content)


async def send_answer_to_support(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()

        support_topic = SupportTopic()
        topic_message = SupportTopicMessage()
        support_topic.id = uuid.uuid4()
        support_topic.responder_telegram_id = message.from_user.id
        support_topic.responder_contacts = data['contact']

        topic_message.topic = support_topic
        topic_message.content = message.text

        create_support_topic(support_topic)
        create_support_topic_message(topic_message)

        await message.answer('✅Ваш ответ отправлен в поддержку.✅\n'
                             'Содержание ответа: \n'
                             f'```\n{message.text}\n```'
                             'Ожидайте ответа!', reply_markup=user_main_keyboard, parse_mode='Markdown')

    except:
        await message.answer('❌Ваш ответ не был отправлен в поддержку.❌\n'
                             'Попробуйте позже!', reply_markup=user_main_keyboard)

    finally:
        await state.finish()


def register_support_handler(dp: Dispatcher):
    dp.register_message_handler(get_support,
                                lambda message: message.text == '☎️ Обратиться в поддержку',
                                state=None)
    dp.register_message_handler(send_answer_to_support, state=SupportState.wait_content)
    dp.register_message_handler(send_contacts, state=SupportState.wait_contact)
