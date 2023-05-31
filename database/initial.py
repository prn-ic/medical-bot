from models import *
import random

db = peewee.PostgresqlDatabase(database=os.getenv('PSQL_DEV_DATABASE'),
                               user=os.getenv('PSQL_DEV_USER'),
                               password=os.getenv('PSQL_DEV_PASSWORD'),
                               host=os.getenv('PSQL_DEV_HOST'),
                               field_types={'uuid': 'uuid'})

if __name__ == '__main__':
    db.create_tables([UserRole,
                      RecordType,
                      EmployeeType,
                      Establishment,
                      User,
                      Employee,
                      EmployeeEstablishment,
                      UserInfo,
                      Question,
                      Record,
                      SupportTopic,
                      SupportTopicMessage,
                      Symptom,
                      SymptomCause,
                      SymptomCauseSolution])
