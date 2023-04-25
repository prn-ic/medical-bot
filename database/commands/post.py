from dotenv import load_dotenv, find_dotenv
from database.models import User, UserInfo, SupportTopic, SupportTopicMessage
import os
import peewee
import uuid

load_dotenv(find_dotenv())
db = peewee.PostgresqlDatabase(database=os.getenv('PSQL_DEV_DATABASE'),
                               user=os.getenv('PSQL_DEV_USER'),
                               password=os.getenv('PSQL_DEV_PASSWORD'),
                               host=os.getenv('PSQL_DEV_HOST'),
                               field_types={'uuid': 'uuid'})


def create_user(user: User):
    User.insert(id=uuid.uuid4() if user.id is None else user.id,
                telegram_id=user.telegram_id).execute()


def create_user_info(user_info: UserInfo):
    UserInfo.insert(id=uuid.uuid4(),
                    role=user_info.role,
                    user=user_info.user,
                    first_name=user_info.first_name,
                    surname=user_info.surname,
                    patronymic=user_info.patronymic,
                    phone=user_info.phone,
                    email=user_info.email,
                    is_notify=False).execute()


def create_support_topic(support_topic: SupportTopic):
    SupportTopic.insert(id=uuid.uuid4() if support_topic.id is None else support_topic.id,
                        responder_telegram_id=support_topic.responder_telegram_id).execute()


def create_support_topic_message(message: SupportTopicMessage):
    SupportTopicMessage.insert(id=uuid.uuid4() if message.id is None else message.id,
                               content=message.content,
                               topic=message.topic).execute()


def close_support_topic(topic_id: uuid):
    SupportTopic.update(is_closed=True).where(SupportTopic.id == topic_id).execute()
