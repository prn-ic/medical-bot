from dotenv import load_dotenv, find_dotenv
from database.models import Question, Establishment
import os
import peewee

load_dotenv(find_dotenv())
db = peewee.PostgresqlDatabase(database=os.getenv('PSQL_DEV_DATABASE'),
                               user=os.getenv('PSQL_DEV_USER'),
                               password=os.getenv('PSQL_DEV_PASSWORD'),
                               host=os.getenv('PSQL_DEV_HOST'),
                               field_types={'uuid': 'uuid'})


def get_question(question_name: str):
    answer = Question.get_or_none(Question.command_name == question_name).answer

    if answer is None:
        return 'Извините, мы не знаем ответ на ваш вопрос'

    return answer


def get_establisments_cities():
    establishments = Establishment.select()
    return [establishment.city_name for establishment in establishments]


def get_establishments_by_city_name(value: str):
    establishments = Establishment.select().where(Establishment.city_name == value)
    return [establishment for establishment in establishments]


def get_establishment_by_name(value: str):
    establishment = Establishment.get_or_none(Establishment.name == value)
    return establishment

