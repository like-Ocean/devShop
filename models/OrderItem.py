from peewee import AutoField, IntegerField, ForeignKeyField
from database import BaseModel
from models import Order, Product


class OrderItem(BaseModel):
    id = AutoField(primary_key=True)
    order = ForeignKeyField(Order, on_delete='CASCADE', null=False)
    product = ForeignKeyField(Product, on_delete='CASCADE', null=False)
    count = IntegerField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'order': {
                'id': self.order.id,
                'user': {
                    'id': self.order.user.id,
                    'first_name': self.order.user.first_name,
                    'surname': self.order.user.surname
                },
                'order_date': self.order.order_date,
                'address': self.order.address,
                'status': self.order.status,
            },
            'product': {
                'id': self.product.id,
                'category': {
                    'name': self.product.category.name
                },
                'name': self.product.name,
                'final_price': self.product.final_price,
            },
            'count': self.count
        }

    class Meta:
        db_table = 'order_items'