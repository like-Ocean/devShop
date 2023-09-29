from peewee import AutoField, IntegerField, ForeignKeyField
from database import BaseModel
from models import Order, Product


class OrderItem(BaseModel):
    id = AutoField(primary_key=True)
    order = ForeignKeyField(Order, on_delete='CASCADE', null=False)
    product = ForeignKeyField(Product, on_delete='CASCADE', null=False)
    count = IntegerField(null=True)

    class Meta:
        db_table = 'order_items'