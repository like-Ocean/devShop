from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel
from models import User


class JWT(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    token = TextField(null=False)
    ref_token = TextField(null=False)

    class Meta:
        db_table = 'jwts'