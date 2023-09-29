from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, Role


class UserRole(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='role', on_delete='CASCADE', null=False)
    role = ForeignKeyField(Role, on_delete='CASCADE', null=False)

    class Meta:
        db_table = 'users_role'