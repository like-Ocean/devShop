from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel
from models import Product


class ProductImg(BaseModel):
    id = AutoField(primary_key=True)
    product = ForeignKeyField(Product, on_delete='CASCADE', null=False)
    url = TextField(null=False)
    filename = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'product': {
                'id': self.product.id,
                'name': self.product.name
            },
            'url': self.url,
            'filename': self.filename
        }

    class Meta:
        db_table = 'product_imgs'