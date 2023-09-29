from peewee import TextField, AutoField, IntegerField, ForeignKeyField, FloatField, Check
from database import BaseModel
from models import Category


class Product(BaseModel):
    id = AutoField(primary_key=True)
    category = ForeignKeyField(Category, backref='category', on_delete='CASCADE', null=False)
    name = TextField(null=False)
    description = TextField(null=False)
    price = FloatField(null=False)
    discount = IntegerField(null=True)
    final_price = FloatField(null=True)
    total_count = IntegerField(null=False, constraints=[Check('count >= 0')])

    def get_dto(self):
        return {
            'id': self.id,
            'category': {
                'id': self.category.id,
                'name': self.category.name
            },
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'discount': self.discount,
            'final_price': self.final_price,
            'total_count': self.total_count
        }

    class Meta:
        db_table = 'products'