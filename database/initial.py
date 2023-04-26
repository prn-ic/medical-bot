from database.models import *
import random


random_uuid_generator = random.Random()

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
