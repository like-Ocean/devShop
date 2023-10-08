from peewee import TextField, AutoField, CharField
from database import BaseModel


class User(BaseModel):
    id = AutoField(primary_key=True)
    first_name = TextField(null=False)
    surname = TextField(null=False)
    phone = TextField(null=True)
    email = CharField(null=False, unique=True, max_length=255)
    password = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'surname': self.surname,
            'phone': self.phone,
            'email': self.email
        }

    class Meta:
        db_table = 'users'