from peewee import TextField, AutoField, ForeignKeyField, DateField
from database import BaseModel
from models import User


class Order(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    order_date = DateField(null=False)
    address = TextField(null=False)
    status = TextField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'surname': self.user.surname
            },
            'order_date': self.order_date,
            'address': self.address,
            'status': self.status,
        }

    class Meta:
        db_table = 'orders'