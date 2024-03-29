from dotenv import load_dotenv, find_dotenv
from database.models import Question, Establishment, UserRole, User, Symptom, SymptomCause, SymptomCauseSolution, Employee, EmployeeEstablishment
import os
import peewee
import difflib
import uuid

load_dotenv(find_dotenv())
db = peewee.PostgresqlDatabase(database=os.getenv('PSQL_DEV_DATABASE'),
                               user=os.getenv('PSQL_DEV_USER'),
                               password=os.getenv('PSQL_DEV_PASSWORD'),
                               host=os.getenv('PSQL_DEV_HOST'),
                               field_types={'uuid': 'uuid'})


def get_question(question_name: str):
    answer = Question.get_or_none(Question.command_name == question_name)

    return answer


def get_answer_by_id(question_id: uuid):
    answer = Question.get_or_none(Question.id == question_id).answer

    return answer


def get_same_answers(question_name: str):
    questions = [question.command_name for question in Question.select()]

    return difflib.get_close_matches(question_name, questions, n=3, cutoff=0.4)


def get_establisment_cities():
    establishments = Establishment.select()
    return [establishment.city_name for establishment in establishments]


def get_establishment_addresses():
    establishments = Establishment.select()
    return [establishments.address for establishment in establishments]


def get_establishments_by_city_name(value: str):
    establishments = Establishment.select().where(Establishment.city_name == value)
    return [establishment for establishment in establishments]


def get_establishment_by_id(value: uuid):
    establishment = Establishment.get_or_none(Establishment.id == value)
    return establishment


def get_user_role_by_name(value: str):
    user_role = UserRole.get_or_none(UserRole.name == value)
    return user_role


def get_user_by_id(value: uuid):
    user = User.get_or_none(User.id == value)
    return user


def get_symptoms():
    return Symptom.select()


def get_cause_by_id(cause_id: uuid):
    cause = SymptomCause.get_or_none(SymptomCause.id == cause_id)
    return cause


def get_symptom_causes(symptom_id: uuid):
    symptom = Symptom.get_or_none(Symptom.id == symptom_id)
    causes = SymptomCause.select().where(SymptomCause.symptom == symptom).order_by(SymptomCause.cause_score)
    return [t for t in causes]


def get_cause_solutions(symptom_id: uuid):
    symptom = Symptom.get_or_none(Symptom.id == symptom_id)
    solutions = SymptomCauseSolution.select().where(SymptomCauseSolution.symptom == symptom) \
        .order_by(SymptomCauseSolution.score)
    return [t for t in solutions]


def get_employees():
    employees = Employee.select()
    return employees


def get_employee_by_id(employee_id: uuid):
    employee = Employee.get_or_none(Employee.id == employee_id)
    return employee


def get_establishment_by_employee_id(employee_id: uuid):
    employee = Employee.get_or_none(Employee.id == employee_id)
    employee_establishment = EmployeeEstablishment.get_or_none(EmployeeEstablishment.employee == employee)
    return employee_establishment.establishment


