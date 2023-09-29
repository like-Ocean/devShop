from peewee import TextField, AutoField, CharField
from database import BaseModel


class Category(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=False, unique=True, max_length=255)
    slug = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }

    class Meta:
        db_table = 'categories'