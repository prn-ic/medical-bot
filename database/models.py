from dotenv import load_dotenv, find_dotenv
import datetime
import os
import peewee

load_dotenv(find_dotenv())
db = peewee.PostgresqlDatabase(database=os.getenv('PSQL_DEV_DATABASE'),
                               user=os.getenv('PSQL_DEV_USER'),
                               password=os.getenv('PSQL_DEV_PASSWORD'),
                               host=os.getenv('PSQL_DEV_HOST'),
                               field_types={'uuid': 'uuid'})


class BaseModel(peewee.Model):
    class Meta:
        database = db

    id = peewee.UUIDField(primary_key=True,
                          unique=True)


class UserRole(BaseModel):
    class Meta:
        db_table = 'user_roles'

    name = peewee.CharField(unique=True)


class RecordType(BaseModel):
    class Meta:
        db_table = 'record_types'

    name = peewee.CharField()


class Establishment(BaseModel):
    class Meta:
        db_table = 'establishments'

    name = peewee.CharField()
    description = peewee.CharField()
    address = peewee.CharField()
    city_name = peewee.CharField()
    coord_latitude = peewee.DecimalField(max_digits=8, decimal_places=6)
    coord_longitude = peewee.DecimalField(max_digits=9, decimal_places=6)


class User(BaseModel):
    class Meta:
        db_table = 'users'

    telegram_id = peewee.CharField(unique=True)
    expiration_time = peewee.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=30))


class UserInfo(BaseModel):
    class Meta:
        db_table = 'user_infos'

    user = peewee.ForeignKeyField(User)
    role = peewee.ForeignKeyField(UserRole)
    first_name = peewee.CharField()
    surname = peewee.CharField()
    patronymic = peewee.CharField()
    phone = peewee.CharField(unique=True)
    email = peewee.CharField(unique=True)
    is_notify = peewee.BooleanField()
    is_accepted = peewee.BooleanField(default=False)


class EmployeeType(BaseModel):
    class Meta:
        db_table = 'employee_types'

    name = peewee.CharField()


class Employee(BaseModel):
    class Meta:
        db_table = 'employees'

    user = peewee.ForeignKeyField(UserInfo, on_delete='cascade')
    type = peewee.ForeignKeyField(EmployeeType)
    position = peewee.CharField()
    link = peewee.CharField()


class Symptom(BaseModel):
    class Meta:
        db_table = 'symptoms'

    name = peewee.CharField()


class SymptomCause(BaseModel):
    class Meta:
        db_table = 'symptom_causes'

    sign = peewee.TextField()
    cause_score = peewee.IntegerField()
    symptom = peewee.ForeignKeyField(Symptom)


class SymptomCauseSolution(BaseModel):
    class Meta:
        db_table = 'symptom_cause_solution'

    name = peewee.TextField()
    indication = peewee.TextField()
    solution = peewee.TextField()
    medic_type = peewee.ForeignKeyField(EmployeeType)
    symptom = peewee.ForeignKeyField(Symptom)
    score = peewee.IntegerField()


class EmployeeEstablishment(BaseModel):
    class Meta:
        db_table = 'employees_establishments'

    employee = peewee.ForeignKeyField(Employee, on_delete='cascade')
    establishment = peewee.ForeignKeyField(Establishment, on_delete='cascade')


class Question(BaseModel):
    class Meta:
        db_table = 'questions'

    command_name = peewee.CharField(unique=True)
    answer = peewee.TextField()


class Record(BaseModel):
    class Meta:
        db_table = 'records'

    record_type = peewee.ForeignKeyField(RecordType, on_delete='cascade')
    visitor = peewee.ForeignKeyField(User, on_delete='cascade')
    medic = peewee.ForeignKeyField(User, on_delete='cascade')
    destination = peewee.DateTimeField()
    note = peewee.CharField(null=True)


class SupportTopic(BaseModel):
    class Meta:
        db_table = 'support_topics'

    responder_telegram_id = peewee.CharField()
    responder_contacts = peewee.CharField()
    is_closed = peewee.BooleanField(default=False)


class SupportTopicMessage(BaseModel):
    class Meta:
        db_table = 'support_topic_messages'

    topic = peewee.ForeignKeyField(SupportTopic)
    content = peewee.TextField()


class Support(BaseModel):
    class Meta:
        db_table = 'supports'

    telegram_id = peewee.CharField()
    is_access = peewee.BooleanField(default=True)
