import uuid

from dotenv import load_dotenv, find_dotenv
import datetime
import os
import peewee
import random


random_uuid_generator = random.Random()

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

    name = peewee.CharField()


class RecordType(BaseModel):
    class Meta:
        db_table = 'record_types'

    name = peewee.CharField()


class Establishment(BaseModel):
    class Meta:
        db_table = 'establishments'

    name = peewee.CharField()
    city_name = peewee.CharField()
    coord_latitude = peewee.DecimalField(max_digits=8, decimal_places=6)
    coord_longitude = peewee.DecimalField(max_digits=9, decimal_places=6)


class User(BaseModel):
    class Meta:
        db_table = 'users'

    telegram_id = peewee.CharField()
    expiration_time = peewee.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=30))


class EmployeeEstablishment(BaseModel):
    class Meta:
        db_table = 'employees_establishments'

    employee = peewee.ForeignKeyField(User, on_delete='cascade')
    establishment = peewee.ForeignKeyField(Establishment, on_delete='cascade')
    room_number = peewee.CharField()


class UserInfo(BaseModel):
    class Meta:
        db_table = 'user_infos'

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

    command_name = peewee.CharField()
    answer = peewee.CharField()


class Record(BaseModel):
    class Meta:
        db_table = 'records'

    record_type = peewee.ForeignKeyField(RecordType, on_delete='cascade')
    visitor = peewee.ForeignKeyField(User, on_delete='cascade')
    medic = peewee.ForeignKeyField(User, on_delete='cascade')
    destination = peewee.DateTimeField()
    note = peewee.CharField(null=True)


if __name__ == '__main__':
    db.create_tables([UserRole,
                      RecordType,
                      Establishment,
                      User,
                      EmployeeEstablishment,
                      UserInfo,
                      Question,
                      Record])

    # Start data
    user_role_source = [
        {'id': uuid.uuid4(), 'name': 'Admin'},
        {'id': uuid.uuid4(), 'name': 'Employee'},
        {'id': uuid.uuid4(), 'name': 'User'},
    ]
    UserRole.insert_many(user_role_source).execute()
