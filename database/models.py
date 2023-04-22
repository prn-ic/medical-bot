from dotenv import load_dotenv, find_dotenv
import datetime
import os
import peewee

load_dotenv(find_dotenv())
db = peewee.PostgresqlDatabase(database=os.getenv('PSQL_DEV_DATABASE'),
                               user=os.getenv('PSQL_DEV_USER'),
                               password=os.getenv('PSQL_DEV_PASSWORD'),
                               host=os.getenv('PSQL_DEV_HOST'))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class UserRole(BaseModel):
    class Meta:
        db_table = 'user_roles'

    id = peewee.UUIDField(primary_key=True, unique=True)
    name = peewee.CharField()


class RecordType(BaseModel):
    class Meta:
        db_table = 'record_types'

    id = peewee.UUIDField(primary_key=True, unique=True)
    name = peewee.CharField()


class Establishment(BaseModel):
    class Meta:
        db_table = 'establishments'

    id = peewee.UUIDField(primary_key=True, unique=True)
    name = peewee.CharField()
    city_name = peewee.CharField()
    coord_latitude = peewee.DecimalField(max_digits=8, decimal_places=6)
    coord_longitude = peewee.DecimalField(max_digits=9, decimal_places=6)


class User(BaseModel):
    class Meta:
        db_table = 'users'

    id = peewee.UUIDField(primary_key=True, unique=True)
    telegram_id = peewee.CharField()
    expiration_time = peewee.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=30))


class EmployeeEstablishment(BaseModel):
    class Meta:
        db_table = 'employees_establishments'

    id = peewee.UUIDField(primary_key=True, unique=True)
    employee = peewee.ForeignKeyField(User)
    establishment = peewee.ForeignKeyField(Establishment)
    room_number = peewee.CharField()


class UserInfo(BaseModel):
    class Meta:
        db_table = 'user_infos'

    id = peewee.UUIDField(primary_key=True, unique=True)
    user = peewee.ForeignKeyField(User)
    role = peewee.ForeignKeyField(UserRole)
    first_name = peewee.CharField()
    surname = peewee.CharField()
    patronymic = peewee.CharField()
    phone = peewee.CharField()
    is_notify = peewee.BooleanField()


class Question(BaseModel):
    class Meta:
        db_table = 'questions'

    id = peewee.UUIDField(primary_key=True, unique=True)
    command_name = peewee.CharField()
    answer = peewee.CharField()


class Record(BaseModel):
    class Meta:
        db_table = 'records'

    id = peewee.UUIDField(primary_key=True, unique=True)
    record_type = peewee.ForeignKeyField(RecordType)
    visitor = peewee.ForeignKeyField(User)
    medic = peewee.ForeignKeyField(User)
    destination = peewee.DateTimeField()
    note = peewee.CharField(null=True)


def migrate():
    db.create_tables([UserRole, RecordType, Establishment, User, EmployeeEstablishment, UserInfo, Question, Record])
