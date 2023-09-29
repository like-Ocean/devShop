from peewee import TextField, AutoField
from database import BaseModel


class Role(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    slug = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'role': self.name,
            'slug': self.slug
        }

    class Meta:
        db_table = 'roles'